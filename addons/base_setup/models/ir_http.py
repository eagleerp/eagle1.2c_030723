# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.
from eagle import models
from eagle.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super(IrHttp, self).session_info()
        result['show_effect'] = request.env['ir.config_parameter'].sudo().get_param('base_setup.show_effect')
        return result
