# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.
from eagle import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    digest_emails = fields.Boolean(string="Digest Emails", config_parameter='digest.default_digest_emails')
    digest_id = fields.Many2one('digest.digest', string='Digest Email', config_parameter='digest.default_digest_id')
