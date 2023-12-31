# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

{
    'name': 'Hong Kong - Accounting',
    'version': '1.0',
    'category': 'Localization',
    'description': """ This is the base module to manage chart of accounting and localization for Hong Kong """,
    'author': 'Eagle ERP',
    'depends': ['account'],
    'data': [
        'data/account_chart_template_data.xml',
        'data/account.account.template.csv',
        'data/l10n_hk_chart_data.xml',
        'data/account_chart_template_configure_data.xml',
    ],
    'license': 'LGPL-3',
}
