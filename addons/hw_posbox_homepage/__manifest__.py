# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

{
    'name': 'IoT Box Homepage',
    'category': 'Sales/Point Of Sale',
    'sequence': 6,
    'website': 'https://www.eagle-erp.com/page/point-of-sale-hardware',
    'summary': 'A homepage for the IoT Box',
    'description': """
IoT Box Homepage
================

This module overrides Eagle web interface to display a simple
Homepage that explains what's the iotbox and shows the status,
and where to find documentation.

If you activate this module, you won't be able to access the 
regular Eagle interface anymore.

""",
    'depends': ['hw_proxy'],
    'installable': False,
    'license': 'LGPL-3',
}
