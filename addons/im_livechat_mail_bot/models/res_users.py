# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

from eagle import models, fields


class Users(models.Model):
    _inherit = 'res.users'
    eaglebot_state = fields.Selection(
        selection_add=[
            ('onboarding_canned', 'Onboarding canned'),
        ])
