# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

import eagle.tests


@eagle.tests.tagged('post_install','-at_install')
class TestUi(eagle.tests.HttpCase):

    def test_01_crm_tour(self):
        self.phantom_js("/web", "eagle.__DEBUG__.services['web_tour.tour'].run('crm_tour')", "eagle.__DEBUG__.services['web_tour.tour'].tours.crm_tour.ready", login="admin")
