# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

{
    "name" : "Norway - Accounting",
    "version" : "2.0",
    "author" : "Rolv Råen",
    'category': 'Localization',
    "description": """This is the module to manage the accounting chart for Norway in Eagle.

Updated for Eagle 9 by Bringsvor Consulting AS <www.bringsvor.com>
""",
    "depends" : [
        "account",
        "base_iban",
        "base_vat",
    ],
    "data": ['data/l10n_no_chart_data.xml',
             'data/account_data.xml',
             'data/account_tax_data.xml',
             'data/account_chart_template_data.xml'],
    "active": False,
    'post_init_hook': '_preserve_tag_on_taxes',
    'license': 'LGPL-3',
}
