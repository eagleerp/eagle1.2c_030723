# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

{
    'name': 'Web',
    'category': 'Hidden',
    'version': '1.0',
    'description':
        """
Eagle Web core module.
========================

This module provides the core of the Eagle Web Client.
        """,
    'depends': ['base'],
    'auto_install': True,
    'data': [
        'security/ir.model.access.csv',
        'views/webclient_templates.xml',
        'views/report_templates.xml',
        'data/res_company.xml',
        'data/report_layout.xml',
    ],
    'qweb': [
        "static/src/xml/base.xml",
        "static/src/xml/kanban.xml",
        "static/src/xml/menu.xml",
        "static/src/xml/pie_chart.xml",
        "static/src/xml/rainbow_man.xml",
        "static/src/xml/report.xml",
        "static/src/xml/web_calendar.xml",
    ],
    'bootstrap': True,  # load translations for login screen,
    'license': 'LGPL-3',
}
