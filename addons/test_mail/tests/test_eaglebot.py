# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

from unittest.mock import patch

from eagle.addons.test_mail.tests.common import BaseFunctionalTest, MockEmails, TestRecipients
from eagle.tools import mute_logger
from eagle.tests import tagged


@tagged("eaglebot")
class TestEaglebot(BaseFunctionalTest, MockEmails, TestRecipients):

    def setUp(self):
        super(TestEaglebot, self).setUp()
        self.eaglebot = self.env.ref("base.partner_root")
        self.message_post_default_kwargs = {
            'body': '',
            'attachment_ids': [],
            'message_type': 'comment',
            'partner_ids': [],
            'subtype': 'mail.mt_comment'
        }
        self.eaglebot_ping_body = '<a href="http://eagle-erp.com/web#model=res.partner&amp;id=%s" class="o_mail_redirect" data-oe-id="%s" data-oe-model="res.partner" target="_blank">@EagleBot</a>' % (self.eaglebot.id, self.eaglebot.id)
        self.test_record_employe = self.test_record.sudo(self.user_employee)

    @mute_logger('eagle.addons.mail.models.mail_mail')
    def test_fetch_listener(self):
        channel = self.env['mail.channel'].sudo(self.user_employee).init_eaglebot()
        partners = self.env['mail.channel'].channel_fetch_listeners(channel.uuid)
        eaglebot = self.env.ref("base.partner_root")
        eaglebot_in_fetch_listeners = [partner for partner in partners if partner['id'] == eaglebot.id]
        self.assertEqual(len(eaglebot_in_fetch_listeners), 1, 'eaglebot should appear only once in channel_fetch_listeners')

    @mute_logger('eagle.addons.mail.models.mail_mail')
    def test_eaglebot_ping(self):
        kwargs = self.message_post_default_kwargs.copy()
        kwargs.update({'body': self.eaglebot_ping_body, 'partner_ids': [self.eaglebot.id, self.user_admin.partner_id.id]})

        with patch('random.choice', lambda x: x[0]):
            self.assertNextMessage(
                self.test_record_employe.with_context({'mail_post_autofollow': True}).message_post(**kwargs),
                sender=self.eaglebot,
                answer=["Yep, EagleBot is in the place!"]
            )
        # Eaglebot should not be a follower but user_employee and user_admin should
        follower = self.test_record.message_follower_ids.mapped('partner_id')
        self.assertNotIn(self.eaglebot, follower)
        self.assertIn(self.user_employee.partner_id, follower)
        self.assertIn(self.user_admin.partner_id, follower)

    @mute_logger('eagle.addons.mail.models.mail_mail')
    def test_onboarding_flow(self):
        kwargs = self.message_post_default_kwargs.copy()
        channel = self.env['mail.channel'].sudo(self.user_employee).init_eaglebot()

        kwargs['body'] = 'tagada 😊'
        self.assertNextMessage(
            channel.message_post(**kwargs),
            sender=self.eaglebot,
            answer=("attachment",)
        )
        kwargs['body'] = ''
        kwargs['attachment_ids'] = [1]
        last_message = self.assertNextMessage(
            channel.message_post(**kwargs),
            sender=self.eaglebot,
            answer=("help",)
        )
        kwargs['attachment_ids'] = []

        channel.execute_command(command="help")
        self.assertNextMessage(
            last_message,  # no message will be post with command help, use last eaglebot message instead
            sender=self.eaglebot,
            answer=("@EagleBot",)
        )
        # we dont test the end of the flow since it will depends of the installed apps (livechat)
        self.user_employee.eaglebot_state = "idle"
        kwargs['partner_ids'] = []
        kwargs['body'] = "I love you"
        self.assertNextMessage(
            channel.message_post(**kwargs),
            sender=self.eaglebot,
            answer=("too human for me",)
        )
        kwargs['body'] = "Go fuck yourself"
        self.assertNextMessage(
            channel.message_post(**kwargs),
            sender=self.eaglebot,
            answer=("I have feelings",)
        )

    @mute_logger('eagle.addons.mail.models.mail_mail')
    def test_eaglebot_no_default_answer(self):
        kwargs = self.message_post_default_kwargs.copy()
        kwargs.update({'body': "I'm not talking to @eaglebot right now", 'partner_ids': []})
        self.assertNextMessage(
            self.test_record_employe.message_post(**kwargs),
            answer=False
        )

    def assertNextMessage(self, message, answer=None, sender=None):
        last_message = self.env['mail.message'].search([('id', '=', message.id + 1)])
        if last_message:
            body = last_message.body.replace('<p>', '').replace('</p>', '')
        else:
            self.assertFalse(answer, "No last message found when an answer was expect")
        if answer is not None:
            if answer and not last_message:
                self.assertTrue(False, "No last message found")
            if isinstance(answer, list):
                self.assertIn(body, answer)
            elif isinstance(answer, tuple):
                for elem in answer:
                    self.assertIn(elem, body)
            elif not answer:
                self.assertFalse(last_message, "No answer should have been post")
                return
            else:
                self.assertEqual(body, answer)
        if sender:
            self.assertEqual(sender, last_message.author_id)
        return last_message
