# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

from eagle import models, _


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    def _compute_dashboard_button_name(self):
        super(CrmTeam, self)._compute_dashboard_button_name()
        self.filtered(lambda team: team.use_opportunities and team.team_type in ('sales', 'website')).update({'dashboard_button_name': _("Pipeline")})
