# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

{
    'name' : 'Analytic Accounting',
    'version': '1.1',
    'category': 'Hidden/Dependency',
    'depends' : ['base', 'decimal_precision', 'mail', 'uom'],
    'description': """
Module for defining analytic accounting object.
===============================================

In Eagle, analytic accounts are linked to general accounts but are treated
totally independently. So, you can enter various different analytic operations
that have no counterpart in the general financial accounts.
    """,
    'data': [
        'security/analytic_security.xml',
        'security/ir.model.access.csv',
        'views/analytic_account_views.xml',
    ],
    'demo': [
        'data/analytic_demo.xml',
        'data/analytic_account_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
