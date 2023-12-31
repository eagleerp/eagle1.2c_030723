# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

from eagle.tests.common import TransactionCase
from eagle.tools import mute_logger


class TestProcRule(TransactionCase):

    def test_proc_rule(self):
        # Create a product route containing a stock rule that will
        # generate a move from Stock for every procurement created in Output
        product_route = self.env['stock.location.route'].create({
            'name': 'Stock -> output route',
            'product_selectable': True,
            'rule_ids': [(0, 0, {
                'name': 'Stock -> output rule',
                'action': 'pull',
                'picking_type_id': self.ref('stock.picking_type_internal'),
                'location_src_id': self.ref('stock.stock_location_stock'),
                'location_id': self.ref('stock.stock_location_output'),
            })],
        })

        # Set this route on `product.product_product_3`
        self.env.ref('product.product_product_3').write({
            'route_ids': [(4, product_route.id)]})

        # Create Delivery Order of 10 `product.product_product_3` from Output -> Customer
        product = self.env.ref('product.product_product_3')
        vals = {
            'name': 'Delivery order for procurement',
            'partner_id': self.ref('base.res_partner_2'),
            'picking_type_id': self.ref('stock.picking_type_out'),
            'location_id': self.ref('stock.stock_location_output'),
            'location_dest_id': self.ref('stock.stock_location_customers'),
            'move_lines': [(0, 0, {
                'name': '/',
                'product_id': product.id,
                'product_uom': product.uom_id.id,
                'product_uom_qty': 10.00,
                'procure_method': 'make_to_order',
            })],
        }
        pick_output = self.env['stock.picking'].create(vals)
        pick_output.move_lines.onchange_product_id()

        # Confirm delivery order.
        pick_output.action_confirm()

        # I run the scheduler.
        # Note: If purchase if already installed, the method _run_buy will be called due
        # to the purchase demo data. As we update the stock module to run this test, the
        # method won't be an attribute of stock.procurement at this moment. For that reason
        # we mute the logger when running the scheduler.
        with mute_logger('eagle.addons.stock.models.procurement'):
            self.env['procurement.group'].run_scheduler()

        # Check that a picking was created from stock to output.
        moves = self.env['stock.move'].search([
            ('product_id', '=', self.ref('product.product_product_3')),
            ('location_id', '=', self.ref('stock.stock_location_stock')),
            ('location_dest_id', '=', self.ref('stock.stock_location_output')),
            ('move_dest_ids', 'in', [pick_output.move_lines[0].id])
        ])
        self.assertEqual(len(moves.ids), 1, "It should have created a picking from Stock to Output with the original picking as destination")
