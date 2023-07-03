# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

import eagle.tests


@eagle.tests.tagged('post_install', '-at_install')
class TestUi(eagle.tests.HttpCase):
    def test_admin(self):
        self.phantom_js("/", "eagle.__DEBUG__.services['web_tour.tour'].run('blog')", "eagle.__DEBUG__.services['web_tour.tour'].tours.blog.ready", login='admin')
