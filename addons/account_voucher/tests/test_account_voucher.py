# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

from eagle import tools
from eagle.modules.module import get_resource_path
from eagle.tests import common, Form
import time


class TestAccountVoucher(common.TransactionCase):

    def _load(self, module, *args):
        tools.convert_file(self.cr, 'account_voucher',
                           get_resource_path(module, *args),
                           {}, 'init', False, 'test', self.registry._assertion_report)

    def test_00_account_voucher_flow(self):
        """ Create Account Voucher for Customer and Vendor """
        self._load('account', 'test', 'account_minimal_test.xml')

        # User-groups and References
        partner_id = self.env.ref('base.res_partner_12')
        cash_journal_id = self.env.ref('account_voucher.cash_journal')
        sales_journal_id = self.env.ref('account_voucher.sales_journal')
        account_receivable_id = self.env.ref('account_voucher.a_recv')

        # Create a Account Voucher User
        voucher_user = self.env['res.users'].create({
            'name': 'Voucher Accountant',
            'login': 'vacc',
            'email': 'accountant@yourcompany.com',
            'company_id': self.env.ref('base.main_company').id,
            'groups_id': [(6, 0, [
                self.ref('base.group_partner_manager'),
                self.ref('account.group_account_user'),
                self.ref('account.group_account_invoice'),
            ])]
        })
        Voucher = self.env['account.voucher'].sudo(voucher_user)

        # Create Customer Voucher
        c = Form(Voucher.with_context(default_voucher_type="sale", voucher_type="sale"),
                 view='account_voucher.view_sale_receipt_form')
        c.partner_id = partner_id
        c.journal_id = sales_journal_id
        with c.line_ids.new() as line:
            line.name = "Voucher for Axelor"
            line.account_id = account_receivable_id
            line.price_unit = 1000.0
        account_voucher_customer = c.save()

        # Check Customer Voucher status.
        self.assertEquals(account_voucher_customer.state, 'draft', 'Initially customer voucher should be in the "Draft" state')

        # Validate Customer voucher
        account_voucher_customer.proforma_voucher()
        # Check for Journal Entry of customer voucher
        self.assertTrue(account_voucher_customer.move_id, 'No journal entry created !.')
        # Find related account move line for Customer Voucher.
        customer_voucher_move = account_voucher_customer.move_id

        # Check state of Account move line.
        self.assertEquals(customer_voucher_move.state, 'posted', 'Account move state is incorrect.')
        # Check partner of Account move line.
        self.assertEquals(customer_voucher_move.partner_id, partner_id, 'Partner is incorrect on account move.')
        # Check journal in Account move line.
        self.assertEquals(customer_voucher_move.journal_id, sales_journal_id, 'Journal is incorrect on account move.')
        # Check amount in Account move line.
        self.assertEquals(customer_voucher_move.amount, 1000.0, 'Amount is incorrect in account move.')

        # Create Vendor Voucher
        v = Form(Voucher.with_context(default_voucher_type="purchase", voucher_type="purchase"))
        v.partner_id = partner_id
        v.journal_id = cash_journal_id
        with v.line_ids.new() as line:
            line.name = "Voucher Axelor"
            line.account_id = account_receivable_id
            line.price_unit = 1000.0
        account_voucher_vendor = v.save()

        # Check Vendor Voucher status.
        self.assertEquals(account_voucher_vendor.state, 'draft', 'Initially vendor voucher should be in the "Draft" state')

        # Validate Vendor voucher
        account_voucher_vendor.proforma_voucher()
        # Check for Journal Entry of vendor voucher
        self.assertTrue(account_voucher_vendor.move_id, 'No journal entry created !.')
        # Find related account move line for Vendor Voucher.
        vendor_voucher_move = account_voucher_vendor.move_id

        # Check state of Account move line.
        self.assertEquals(vendor_voucher_move.state, 'posted', 'Account move state is incorrect.')
        # Check partner of Account move line.
        self.assertEquals(vendor_voucher_move.partner_id, partner_id, 'Partner is incorrect on account move.')
        # Check journal in Account move line.
        self.assertEquals(vendor_voucher_move.journal_id, cash_journal_id, 'Journal is incorrect on account move.')
        # Check amount in Account move line.
        self.assertEquals(vendor_voucher_move.amount, 1000.0, 'Amount is incorrect in acccount move.')

    def test_different_account_than_default(self):
        self._load('account', 'test', 'account_minimal_test.xml')

        # User-groups and References
        cash_journal_id = self.env.ref('account_voucher.cash_journal')
        sales_journal_id = self.env.ref('account_voucher.sales_journal')
        account_receivable_id = self.env.ref('account_voucher.a_recv')

        receivable_other = account_receivable_id.copy({
            'name': 'Other Receivable',
            'code': '666',
        })

        income_account = self.env['account.account'].create({
            'name': 'income',
            'code': '999',
            'user_type_id': self.env.ref('account.data_account_type_other_income').id,
        })

        partner = self.env['res.partner'].create({
            'name': 'Ian Anderson',
            'property_account_receivable_id': account_receivable_id.id,
        })

        voucher = self.env['account.voucher'].create({
            'voucher_type': 'sale',
            'partner_id': partner.id,
            'account_id': receivable_other.id,
            'journal_id': sales_journal_id.id,
            'pay_now': 'pay_now',
            'payment_journal_id': cash_journal_id.id,
            'line_ids': [(0, False, {
                'name': 'Test',
                'quantity': 12.0,
                'price_unit': 500,
                'account_id': income_account.id
            })]
        })

        # validation
        voucher.proforma_voucher()

        line_rcv = voucher.move_id.line_ids.filtered(lambda l: l.account_id.internal_type == 'receivable')

        self.assertEquals(line_rcv.account_id, receivable_other)
        self.assertTrue(line_rcv.full_reconcile_id.exists())

        self.assertEquals(len(line_rcv.full_reconcile_id.reconciled_line_ids), 2)
        reconciled_line = line_rcv.full_reconcile_id.reconciled_line_ids - line_rcv
        self.assertEquals(reconciled_line.account_id, receivable_other)
