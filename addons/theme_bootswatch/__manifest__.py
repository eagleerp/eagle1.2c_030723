# -*- encoding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

{
    'name': 'Bootswatch Theme',
    'description': 'Bootswatch themes',
    'category': 'Theme/Corporate',
    'sequence': 900,
    'version': '1.0',
    'depends': ['website', 'website_theme_install'],
    'data': [
        'data/theme_bootswatch_data.xml',
        'views/theme_bootswatch_templates.xml',
    ],
    'images': [
        'static/description/bootswatch.png',
        'static/description/bootswatch_screenshot.jpg',
    ],
    'application': False,
    'license': 'LGPL-3',
}
