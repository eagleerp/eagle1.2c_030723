#-*- coding:utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

# Copyright (C) 2012 Michael Telahun Makonnen <mmakonnen@gmail.com>.

{
    'name': 'Ethiopia - Accounting',
    'version': '2.0',
    'category': 'Localization',
    'description': """
Base Module for Ethiopian Localization
======================================

This is the latest Ethiopian Eagle localization and consists of:
    - Chart of Accounts
    - VAT tax structure
    - Withholding tax structure
    - Regional State listings
    """,
    'author':'Michael Telahun Makonnen <mmakonnen@gmail.com>',
    'website':'http://miketelahun.wordpress.com',
    'depends': [
        'account',
    ],
    'data': [
        'data/l10n_et_chart_data.xml',
        'data/account.account.template.csv',
        'data/account_chart_template_data.xml',
        'data/account_account_tag_data.xml',
        'data/account.tax.group.csv',
        'data/account.tax.template.csv',
        'data/account_chart_template_configure_data.xml',
        'data/res.country.state.csv',
    ],
    'license': 'LGPL-3',
}
