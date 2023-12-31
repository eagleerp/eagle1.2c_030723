# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

{
    'name': 'Gengo Translator',
    'category': 'Website',
    'summary': 'Translate website in one-click',
    'description': """
This module allows to send website content to Gengo translation service in a single click. Gengo then gives back the translated terms in the destination language.
    """,
    'depends': [
        'website',
        'base_gengo'
    ],
    'data': [
        'views/website_gengo_templates.xml',
    ],
    'license': 'LGPL-3',
}
