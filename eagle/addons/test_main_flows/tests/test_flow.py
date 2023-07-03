# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

import eagle.tests


@eagle.tests.tagged('post_install', '-at_install')
class TestUi(eagle.tests.HttpCase):
    
    def test_01_main_flow_tour(self):
        self.phantom_js("/web", "eagle.__DEBUG__.services['web_tour.tour'].run('main_flow_tour')", "eagle.__DEBUG__.services['web_tour.tour'].tours.main_flow_tour.ready", login="admin", timeout=180)
