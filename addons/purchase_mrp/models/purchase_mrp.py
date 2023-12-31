# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

from eagle import fields, models
from eagle.tools import float_compare


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def _get_document_iterate_key(self, move_raw_id):
        return super(MrpProduction, self)._get_document_iterate_key(move_raw_id) or 'created_purchase_line_id'

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _update_received_qty(self):
        kit_lines = self.env['purchase.order.line']
        for line in self.filtered(lambda x: x.move_ids and x.product_id.id not in x.move_ids.mapped('product_id').ids):
            bom = self.env['mrp.bom']._bom_find(product=line.product_id, company_id=line.company_id.id)
            if bom and bom.type == 'phantom':
                line.qty_received = line._get_bom_delivered(bom=bom)
                kit_lines += line
        super(PurchaseOrderLine, self - kit_lines)._update_received_qty()

    def _get_bom_delivered(self, bom=False):
        self.ensure_one()

        # In the case of a kit, we need to check if all components are shipped. Since the BOM might
        # have changed, we don't compute the quantities but verify the move state.
        if bom:
            moves = self.move_ids.filtered(lambda m: m.picking_id and m.picking_id.state != 'cancel')
            bom_delivered = all([move.state == 'done' for move in moves])
            if bom_delivered:
                return self.product_qty
            else:
                return 0.0

    def _get_upstream_documents_and_responsibles(self, visited):
        return [(self.order_id, self.order_id.user_id, visited)]

    def _get_qty_procurement(self):
        self.ensure_one()
        # Specific case when we change the qty on a PO for a kit product.
        # We don't try to be too smart and keep a simple approach: we compare the quantity before
        # and after update, and return the difference. We don't take into account what was already
        # sent, or any other exceptional case.
        bom = self.env['mrp.bom'].sudo()._bom_find(product=self.product_id)
        if bom and bom.type == 'phantom' and 'previous_product_qty' in self.env.context:
            return self.env.context['previous_product_qty'].get(self.id, 0.0)
        return super()._get_qty_procurement()
    
class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_phantom_move_values(self, bom_line, quantity):
        vals = super(StockMove, self)._prepare_phantom_move_values(bom_line, quantity)
        if self.purchase_line_id:
            vals['purchase_line_id'] = self.purchase_line_id.id
        return vals

