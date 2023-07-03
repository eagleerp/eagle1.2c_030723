# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

import eagle.tests

@eagle.tests.tagged('post_install', '-at_install')
class TestUi(eagle.tests.HttpCase):

    def test_01_admin_rte(self):
        self.phantom_js("/web", "eagle.__DEBUG__.services['web_tour.tour'].run('rte')", "eagle.__DEBUG__.services['web_tour.tour'].tours.rte.ready", login='admin')

    def test_02_admin_rte_inline(self):
        self.phantom_js("/web", "eagle.__DEBUG__.services['web_tour.tour'].run('rte_inline')", "eagle.__DEBUG__.services['web_tour.tour'].tours.rte_inline.ready", login='admin')
