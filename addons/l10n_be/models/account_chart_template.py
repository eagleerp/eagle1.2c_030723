# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

from eagle import api, models, fields


class AccountChartTemplate(models.Model):
    _inherit = 'account.chart.template'

    def get_countries_posting_at_bank_rec(self):
        rslt = super(AccountChartTemplate, self).get_countries_posting_at_bank_rec()
        rslt.append('BE')
        return rslt
