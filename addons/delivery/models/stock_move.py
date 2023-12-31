# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

from eagle import api, fields, models

from eagle.addons import decimal_precision as dp


class StockMove(models.Model):
    _inherit = 'stock.move'

    weight = fields.Float(compute='_cal_move_weight', digits=dp.get_precision('Stock Weight'), store=True, compute_sudo=True)

    @api.depends('product_id', 'product_uom_qty', 'product_uom')
    def _cal_move_weight(self):
        for move in self.filtered(lambda moves: moves.product_id.weight > 0.00):
            move.weight = (move.product_qty * move.product_id.weight)

    def _get_new_picking_values(self):
        vals = super(StockMove, self)._get_new_picking_values()
        vals['carrier_id'] = self.sale_line_id.order_id.carrier_id.id
        return vals
