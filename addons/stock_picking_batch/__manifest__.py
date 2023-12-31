# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

{
    'name': 'Warehouse Management: Batch Picking',
    'version': '1.0',
    'category': 'Warehouse',
    'description': """
This module adds the batch picking option in warehouse management
=================================================================
    """,
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_batch_views.xml',
        'data/stock_picking_batch_data.xml',
        'wizard/stock_picking_to_batch_views.xml',
        'report/stock_picking_batch_report_views.xml',
        'report/report_picking_batch.xml',
    ],
    'demo': [
        'data/stock_picking_batch_demo.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
