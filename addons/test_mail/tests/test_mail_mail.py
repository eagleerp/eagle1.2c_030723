# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

import itertools

from eagle.addons.test_mail.tests import common as mail_common
from eagle.tests import common
from eagle.tools import mute_logger
from eagle.addons.base.models.ir_mail_server import MailDeliveryException


class TestMail(common.SavepointCase, mail_common.MockEmails):

    @classmethod
    def setUpClass(cls):
        super(TestMail, cls).setUpClass()

        cls.user_employee = cls.env['res.users'].with_context(mail_common.BaseFunctionalTest._test_context).create({
            'name': 'Ernest Employee',
            'login': 'ernest',
            'email': 'e.e@example.com',
            'signature': '--\nErnest',
            'notification_type': 'email',
            'groups_id': [(6, 0, [cls.env.ref('base.group_user').id])]
        })

    @mute_logger('eagle.addons.mail.models.mail_mail')
    def test_mail_message_notify_from_mail_mail(self):
        # Due ot post-commit hooks, store send emails in every step
        self.email_to_list = []
        mail = self.env['mail.mail'].create({
            'body_html': '<p>Test</p>',
            'email_to': 'test@example.com',
            'partner_ids': [(4, self.user_employee.partner_id.id)]
        })
        self.email_to_list.extend(itertools.chain.from_iterable(sent_email['email_to'] for sent_email in self._mails if sent_email.get('email_to')))
        self.assertNotIn(u'Ernest Employee <e.e@example.com>', self.email_to_list)
        mail.send()
        self.email_to_list.extend(itertools.chain.from_iterable(sent_email['email_to'] for sent_email in self._mails if sent_email.get('email_to')))
        self.assertNotIn(u'Ernest Employee <e.e@example.com>', self.email_to_list)
        self.assertIn(u'test@example.com', self.email_to_list)

    @mute_logger('eagle.addons.mail.models.mail_mail')
    def test_mail_message_values_unicode(self):
        mail = self.env['mail.mail'].create({
            'body_html': '<p>Test</p>',
            'email_to': 'test.😊@example.com',
            'partner_ids': [(4, self.user_employee.partner_id.id)]
        })

        self.assertRaises(MailDeliveryException, lambda: mail.send(raise_exception=True))
