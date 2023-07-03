# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.
import eagle.tests


@eagle.tests.common.at_install(False)
@eagle.tests.common.post_install(True)
class TestUi(eagle.tests.HttpCase):
    def test_01_wishlist_tour(self):
        self.phantom_js("/", "eagle.__DEBUG__.services['web_tour.tour'].run('shop_wishlist')", "eagle.__DEBUG__.services['web_tour.tour'].tours.shop_wishlist.ready")
