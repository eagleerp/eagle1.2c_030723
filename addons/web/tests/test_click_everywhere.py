# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

import eagle.tests


@eagle.tests.tagged('click_all', 'post_install', '-at_install', '-standard')
class TestMenusAdmin(eagle.tests.HttpCase):

    def test_01_click_everywhere_as_admin(self):
        self.browser_js("/web", "eagle.__DEBUG__.services['web.clickEverywhere']();", "eagle.isReady === true", login="admin", timeout=45*60)


@eagle.tests.tagged('click_all', 'post_install', '-at_install', '-standard')
class TestMenusDemo(eagle.tests.HttpCase):

    def test_01_click_everywhere_as_demo(self):
        self.browser_js("/web", "eagle.__DEBUG__.services['web.clickEverywhere']();", "eagle.isReady === true", login="demo", timeout=1800)
