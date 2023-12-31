# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.


{
    "name": "Vietnam - Accounting",
    "version": "2.0",
    "author": "General Solutions",
    'website': 'http://gscom.vn',
    'category': 'Localization',
    "description": """
This is the module to manage the accounting chart for Vietnam in Eagle.
=========================================================================

This module applies to companies based in Vietnamese Accounting Standard (VAS)
with Chart of account under Circular No. 200/2014/TT-BTC

**Credits:**
    - General Solutions.
    - Trobz
""",
    "depends": [
        "account",
        "base_iban"
    ],
    "data": [
         'data/res.country.state.csv',
         'data/l10n_vn_chart_data.xml',
         'data/account.account.template.csv',
         'data/l10n_vn_chart_post_data.xml',
         'data/account_data.xml',
         'data/account_tax_data.xml',
         'data/account_chart_template_data.xml',
    ],
    'post_init_hook': '_preserve_tag_on_taxes',
    'license': 'LGPL-3',
}
