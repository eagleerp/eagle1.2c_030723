# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

import eagle.tests


@eagle.tests.common.tagged('post_install', '-at_install')
class TestUi(eagle.tests.HttpCase):

    def setUp(self):
        super(TestUi, self).setUp()
        # create a template
        product_template = self.env['product.template'].create({
            'name': 'Test Product',
            'website_published': True,
            'list_price': 750,
        })

        tax = self.env['account.tax'].create({'name': "Test tax", 'amount': 10})
        product_template.taxes_id = tax

        product_attribute = self.env.ref('product.product_attribute_1')
        product_attribute_value_1 = self.env.ref('product.product_attribute_value_1')
        product_attribute_value_2 = self.env.ref('product.product_attribute_value_2')

        # set attribute and attribute values on the template
        self.env['product.template.attribute.line'].create([{
            'attribute_id': product_attribute.id,
            'product_tmpl_id': product_template.id,
            'value_ids': [(6, 0, [product_attribute_value_1.id, product_attribute_value_2.id])]
        }])

        # set a different price on the variants to differentiate them
        product_template_attribute_values = self.env['product.template.attribute.value'] \
            .search([('product_tmpl_id', '=', product_template.id)])

        for ptav in product_template_attribute_values:
            if ptav.name == "Steel":
                ptav.price_extra = 0
            else:
                ptav.price_extra = 50.4

        product_template.create_variant_ids()

    def test_01_admin_shop_customize_tour(self):
        self.phantom_js("/", "eagle.__DEBUG__.services['web_tour.tour'].run('shop_customize')", "eagle.__DEBUG__.services['web_tour.tour'].tours.shop_customize.ready", login="admin")

    def test_02_admin_shop_custom_attribute_value_tour(self):
        # Make sure pricelist rule exist
        product_template = self.env.ref('product.product_product_4_product_template')

        # fix runbot, sometimes one pricelist is chosen, sometimes the other...
        pricelists = self.env['website'].get_current_website().get_current_pricelist() | self.env.ref('product.list0')

        for pricelist in pricelists:
            if not pricelist.item_ids.filtered(lambda i: i.product_tmpl_id == product_template and i.price_discount == 20):
                self.env['product.pricelist.item'].create({
                    'base': 'list_price',
                    'applied_on': '1_product',
                    'pricelist_id': pricelist.id,
                    'product_tmpl_id': product_template.id,
                    'price_discount': 20,
                    'min_quantity': 2,
                    'compute_price': 'formula',
                })

            pricelist.discount_policy = 'without_discount'

        self.phantom_js("/", "eagle.__DEBUG__.services['web_tour.tour'].run('shop_custom_attribute_value')", "eagle.__DEBUG__.services['web_tour.tour'].tours.shop_custom_attribute_value.ready", login="admin")

    def test_03_public_tour_shop_dynamic_variants(self):
        """ The goal of this test is to make sure product variants with dynamic
        attributes can be created by the public user (when being added to cart).
        """

        # create the attribute
        product_attribute = self.env['product.attribute'].create({
            'name': "Dynamic Attribute",
            'create_variant': 'dynamic',
        })

        # create the attribute values
        product_attribute_values = self.env['product.attribute.value'].create([{
            'name': "Dynamic Value 1",
            'attribute_id': product_attribute.id,
            'sequence': 1,
        }, {
            'name': "Dynamic Value 2",
            'attribute_id': product_attribute.id,
            'sequence': 2,
        }])

        # create the template
        product_template = self.env['product.template'].create({
            'name': 'Dynamic Product',
            'website_published': True,
            'list_price': 0,
        })

        # set attribute and attribute values on the template
        self.env['product.template.attribute.line'].create([{
            'attribute_id': product_attribute.id,
            'product_tmpl_id': product_template.id,
            'value_ids': [(6, 0, product_attribute_values.ids)]
        }])

        # set a different price on the variants to differentiate them
        product_template_attribute_values = self.env['product.template.attribute.value'] \
            .search([('product_tmpl_id', '=', product_template.id)])

        for ptav in product_template_attribute_values:
            if ptav.name == "Dynamic Value 1":
                ptav.price_extra = 10
            else:
                # 0 to not bother with the pricelist of the public user
                ptav.price_extra = 0

        self.phantom_js("/", "eagle.__DEBUG__.services['web_tour.tour'].run('tour_shop_dynamic_variants')", "eagle.__DEBUG__.services['web_tour.tour'].tours.tour_shop_dynamic_variants.ready")

    def test_04_portal_tour_deleted_archived_variants(self):
        """The goal of this test is to make sure deleted and archived variants
        are shown as impossible combinations.

        Using "portal" to have various users in the tests.
        """

        # create the attribute
        product_attribute = self.env['product.attribute'].create({
            'name': "My Attribute",
            'create_variant': 'always',
        })

        # create the attribute values
        product_attribute_values = self.env['product.attribute.value'].create([{
            'name': "My Value 1",
            'attribute_id': product_attribute.id,
            'sequence': 1,
        }, {
            'name': "My Value 2",
            'attribute_id': product_attribute.id,
            'sequence': 2,
        }, {
            'name': "My Value 3",
            'attribute_id': product_attribute.id,
            'sequence': 3,
        }])

        # create the template
        product_template = self.env['product.template'].create({
            'name': 'Test Product 2',
            'website_published': True,
        })

        # set attribute and attribute values on the template
        self.env['product.template.attribute.line'].create([{
            'attribute_id': product_attribute.id,
            'product_tmpl_id': product_template.id,
            'value_ids': [(6, 0, product_attribute_values.ids)]
        }])

        # set a different price on the variants to differentiate them
        product_template_attribute_values = self.env['product.template.attribute.value'] \
            .search([('product_tmpl_id', '=', product_template.id)])

        product_template_attribute_values[0].price_extra = 10
        product_template_attribute_values[1].price_extra = 20
        product_template_attribute_values[2].price_extra = 30

        product_template.create_variant_ids()

        # archive first combination (first variant)
        product_template.product_variant_ids[0].active = False
        # delete second combination (which is now first variant since cache has been cleared)
        product_template.product_variant_ids[0].unlink()

        self.phantom_js("/", "eagle.__DEBUG__.services['web_tour.tour'].run('tour_shop_deleted_archived_variants')", "eagle.__DEBUG__.services['web_tour.tour'].tours.tour_shop_deleted_archived_variants.ready", login="portal")

    def test_05_demo_tour_no_variant_attribute(self):
        """The goal of this test is to make sure attributes no_variant are
        correctly added to cart.

        Using "demo" to have various users in the tests.
        """

        # create the attribute
        product_attribute_no_variant = self.env['product.attribute'].create({
            'name': "No Variant Attribute",
            'create_variant': 'no_variant',
        })

        # create the attribute value
        product_attribute_value_no_variant = self.env['product.attribute.value'].create({
            'name': "No Variant Value",
            'attribute_id': product_attribute_no_variant.id,
        })

        # create the template
        product_template = self.env['product.template'].create({
            'name': 'Test Product 3',
            'website_published': True,
        })

        # set attribute and attribute value on the template
        ptal = self.env['product.template.attribute.line'].create([{
            'attribute_id': product_attribute_no_variant.id,
            'product_tmpl_id': product_template.id,
            'value_ids': [(6, 0, product_attribute_value_no_variant.ids)]
        }])

        # set a price on the value
        ptal.product_template_value_ids.price_extra = 10

        product_template.create_variant_ids()

        self.phantom_js("/", "eagle.__DEBUG__.services['web_tour.tour'].run('tour_shop_no_variant_attribute')", "eagle.__DEBUG__.services['web_tour.tour'].tours.tour_shop_no_variant_attribute.ready", login="demo")

    def test_06_admin_list_view_b2c(self):
        # activate b2c
        config = self.env['res.config.settings'].create({})
        config.show_line_subtotals_tax_selection = "tax_included"
        config._onchange_sale_tax()
        config.execute()

        self.browser_js("/", "eagle.__DEBUG__.services['web_tour.tour'].run('shop_list_view_b2c')", "eagle.__DEBUG__.services['web_tour.tour'].tours.shop_list_view_b2c.ready", login="admin")
