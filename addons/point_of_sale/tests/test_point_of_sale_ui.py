# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

import eagle.tests


@eagle.tests.tagged('post_install', '-at_install')
class TestUi(eagle.tests.HttpCase):

    def test_01_point_of_sale_tour(self):
        self.phantom_js("/web", "eagle.__DEBUG__.services['web_tour.tour'].run('point_of_sale_tour')", "eagle.__DEBUG__.services['web_tour.tour'].tours.point_of_sale_tour.ready", login="admin")
