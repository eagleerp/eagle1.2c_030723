# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

from . import controllers
from . import models
from . import report
from . import wizard

from eagle import api, SUPERUSER_ID


def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    teams = env['crm.team'].search([('dashboard_graph_model', 'in', ['crm.opportunity.report', 'crm.lead'])])
    teams.update({'dashboard_graph_model': None})
