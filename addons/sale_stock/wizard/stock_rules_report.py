# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

from eagle import api, fields, models


class StockRulesReport(models.TransientModel):
    _inherit = 'stock.rules.report'

    so_route_ids = fields.Many2many('stock.location.route', string='Apply specific rotues',
        domain="[('sale_selectable', '=', True)]", help="Choose to apply SO lines specific routes.")

    def _prepare_report_data(self):
        data = super(StockRulesReport, self)._prepare_report_data()
        data['so_route_ids'] = self.so_route_ids.ids
        return data
