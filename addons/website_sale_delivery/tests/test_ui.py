import eagle.tests
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.


@eagle.tests.tagged('post_install', '-at_install')
class TestUi(eagle.tests.HttpCase):

    def test_01_free_delivery_when_exceed_threshold(self):
        self.env.ref("delivery.free_delivery_carrier").write({
            'fixed_price': 2,
            'free_over': True,
            'amount': 10,
        })
        self.phantom_js("/", "eagle.__DEBUG__.services['web_tour.tour'].run('check_free_delivery')", "eagle.__DEBUG__.services['web_tour.tour'].tours.check_free_delivery.ready", login="admin")
