# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

from eagle import models


class StockQuantityHistory(models.TransientModel):
    _inherit = 'stock.quantity.history'

    def open_table(self):
        if not self.env.context.get('valuation'):
            return super(StockQuantityHistory, self).open_table()

        self.env['stock.move']._run_fifo_vacuum()

        if self.compute_at_date:
            tree_view_id = self.env.ref('stock_account.view_stock_product_tree2').id
            form_view_id = self.env.ref('stock.product_form_view_procurement_button').id
            # We pass `to_date` in the context so that `qty_available` will be computed across
            # moves until date.
            action = self.env.ref('stock_account.product_valuation_action').read()[0]
            action['views'] = [(tree_view_id, 'tree'), (form_view_id, 'form')]
            action['context'] = dict(self.env.context, to_date=self.date, company_owned=True, create=False, edit=False)
            return action
        else:
            return self.env.ref('stock_account.product_valuation_action').read()[0]

