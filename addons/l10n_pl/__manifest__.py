# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

# Copyright (C) 2009 - now Grzegorz Grzelak grzegorz.grzelak@openglobe.pl

{
    'name' : 'Poland - Accounting',
    'version' : '2.0',
    'author' : 'Grzegorz Grzelak (OpenGLOBE)',
    'website': 'http://www.openglobe.pl',
    'category': 'Localization',
    'description': """
This is the module to manage the accounting chart and taxes for Poland in Eagle.
==================================================================================

To jest moduł do tworzenia wzorcowego planu kont, podatków, obszarów podatkowych i
rejestrów podatkowych. Moduł ustawia też konta do kupna i sprzedaży towarów
zakładając, że wszystkie towary są w obrocie hurtowym.

Niniejszy moduł jest przeznaczony dla eagle 8.0.
Wewnętrzny numer wersji OpenGLOBE 1.02
    """,
    'depends' : [
        'account',
        'base_iban',
        'base_vat',
    ],
    'data': [
              'data/l10n_pl_chart_data.xml',
              'data/account.account.template.csv',
              'data/l10n_pl_chart_post_data.xml',
              'data/account_data.xml',
              'data/account_tax_data.xml',
              'data/account_fiscal_position_data.xml',
              'data/res_country_state_data.xml',
              'data/account_chart_template_data.xml'
    ],
    'post_init_hook': '_preserve_tag_on_taxes',
    'license': 'LGPL-3',
}
