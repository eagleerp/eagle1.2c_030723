# -*- coding: utf-8 -*-
# Part of Eagle ERP. See LICENSE file for full copyright and licensing details.

{
    'name': 'Accounting',
    'version': '12.0.3.2.0',
    'category': 'Accounting',
    'summary': 'Accounting Reports, Asset Management and Account Budget For Eagle12 Community Edition',
    'sequence': '8',
    'author': 'Eagle ERP',
    'website': 'http://eagle-erp.com',
    'maintainer': 'Eagle ERP',
    'support': 'eagle.erp.com@gmail.com',
    'website': '',
    'depends': ['accounting_pdf_reports', 'eagle_account_asset', 'eagle_account_budget'],
    'demo': [],
    'data': [
        'wizard/change_lock_date.xml',
        'views/account.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.gif'],
    'qweb': [],
}
