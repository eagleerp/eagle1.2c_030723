# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

{
    'name': 'Payment Acquirer',
    'category': 'Accounting',
    'summary': 'Payment Acquirer Base Module',
    'version': '1.0',
    'description': """Payment Acquirer Base Module""",
    'depends': ['account'],
    'data': [
        'data/account_data.xml',
        'data/payment_icon_data.xml',
        'data/payment_acquirer_data.xml',
        'data/payment_cron.xml',
        'views/payment_views.xml',
        'views/account_payment_views.xml',
        'views/account_invoice_views.xml',
        'views/payment_acquirer_onboarding_templates.xml',
        'views/payment_templates.xml',
        'views/payment_portal_templates.xml',
        'views/assets.xml',
        'views/res_partner_views.xml',
        'security/ir.model.access.csv',
        'security/payment_security.xml',
    ],
    'installable': True,
    'auto_install': True,
    'uninstall_hook': 'uninstall_hook',
    'license': 'LGPL-3',
}
