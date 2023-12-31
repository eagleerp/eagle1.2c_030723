# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

from eagle.addons.test_mail.tests.common import BaseFunctionalTest, TestRecipients
from eagle.tests import tagged, users


@tagged('mail_tools')
class TestMessageModeration(BaseFunctionalTest, TestRecipients):

    @classmethod
    def setUpClass(cls):
        super(TestMessageModeration, cls).setUpClass()

        cls._test_email = 'alfredoastaire@test.example.com'
        cls.test_partner = cls.env['res.partner'].create({
            'country_id': cls.env.ref('base.be').id,
            'email': cls._test_email,
            'mobile': '0456001122',
            'name': 'Alfred Astaire',
            'phone': '0456334455',
        })

    @users('ernest')
    def test_find_partner_from_emails(self):
        Partner = self.env['res.partner']
        test_partner = Partner.browse(self.test_partner.ids)
        self.assertEqual(test_partner.email, self._test_email)

        # test direct match
        found = Partner._find_partner_from_emails([self._test_email])
        self.assertEqual(found, test_partner.ids)

        # test encapsulated email
        found = Partner._find_partner_from_emails(['"Norbert Poiluchette" <%s>' % self._test_email])
        self.assertEqual(found, test_partner.ids)

        # test with wildcard "_"
        found = Partner._find_partner_from_emails(['alfred_astaire@test.example.com'])
        self.assertEqual(found, [False])

        # sub-check: this search effectively consider _ as a wildcard
        found = Partner._search_on_partner('alfred_astaire@test.example.com')
        self.assertEqual(found, test_partner.id)

        # test partners with encapsulated emails
        # ------------------------------------------------------------
        test_partner.sudo().write({'email': '"Alfred Mighty Power Astaire" <%s>' % self._test_email})

        # test direct match
        found = Partner._find_partner_from_emails([self._test_email])
        self.assertEqual(found, test_partner.ids)

        # test encapsulated email
        found = Partner._find_partner_from_emails(['"Norbert Poiluchette" <%s>' % self._test_email])
        self.assertEqual(found, test_partner.ids)

        # test with wildcard "_"
        found = Partner._find_partner_from_emails(['alfred_astaire@test.example.com'])
        self.assertEqual(found, [False])

        # sub-check: this search effectively consider _ as a wildcard
        found = Partner._search_on_partner('alfred_astaire@test.example.com')
        self.assertEqual(found, test_partner.id)

        # test partners with look-alike emails
        # ------------------------------------------------------------
        for email_lookalike in [
                'alfred.astaire@test.example.com',
                'alfredoastaire@example.com',
                'aalfredoastaire@test.example.com',
                'alfredoastaire@test.example.comm']:
            test_partner.sudo().write({'email': '"Alfred Astaire" <%s>' % email_lookalike})

            # test direct match
            found = Partner._find_partner_from_emails([self._test_email])
            self.assertEqual(found, [False])
            # test encapsulated email
            found = Partner._find_partner_from_emails(['"Norbert Poiluchette" <%s>' % self._test_email])
            self.assertEqual(found, [False])
            # test with wildcard "_"
            found = Partner._find_partner_from_emails(['alfred_astaire@test.example.com'])
            self.assertEqual(found, [False])
