# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

# Copyright (c) 2011 Noviat nv/sa (www.noviat.be). All rights reserved.

{
    'name': 'Belgium - Structured Communication',
    'version': '1.2',
    'author': 'Noviat',
    'category': 'Invoicing Management',
    'description': """

Add Structured Communication to customer invoices.
--------------------------------------------------

Using BBA structured communication simplifies the reconciliation between invoices and payments.
You can select the structured communication as payment communication in Invoicing/Accounting settings.
Three algorithms are suggested:

    1) Random : +++RRR/RRRR/RRRDD+++
        **R..R =** Random Digits, **DD =** Check Digits
    2) Date : +++DOY/YEAR/SSSDD+++
        **DOY =** Day of the Year, **SSS =** Sequence Number, **DD =** Check Digits
    3) Customer Reference +++RRR/RRRR/SSSDDD+++
        **R..R =** Customer Reference without non-numeric characters, **SSS =** Sequence Number, **DD =** Check Digits
    """,
    'depends': ['account', 'l10n_be'],
    'data' : [
        'data/mail_template_data.xml',
        'views/res_config_settings_views.xml',
    ],
    'auto-install': True,
    'license': 'LGPL-3',
}
