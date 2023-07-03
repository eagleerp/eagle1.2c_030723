# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

from eagle import models, fields, api, _
from eagle.exceptions import ValidationError


class PosConfig(models.Model):
    _inherit = 'pos.config'

    rounding_method = fields.Many2one('account.cash.rounding', string="Cash rounding", domain=[('strategy', '=', 'add_invoice_line')])
    cash_rounding = fields.Boolean(string="Cash Rounding")
    only_round_cash_method = fields.Boolean(string="Only apply rounding on cash")


    @api.constrains('rounding_method')
    def _check_rounding_method_strategy(self):
        if self.cash_rounding and self.rounding_method.strategy != 'add_invoice_line':
            raise ValidationError(_("Cash rounding strategy must be: 'Add a rounding line'"))
