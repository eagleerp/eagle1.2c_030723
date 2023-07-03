# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

import time

from unittest.mock import ANY, Mock, patch

from eagle.exceptions import ValidationError
from eagle.tests.common import SavepointCase


class TestFetchmailOutlook(SavepointCase):

    @patch('eagle.addons.fetchmail.models.fetchmail.IMAP4_SSL')
    def test_connect(self, mock_imap):
        """Test that the connect method will use the right
        authentication method with the right arguments.
        """
        mock_connection = Mock()
        mock_imap.return_value = mock_connection

        mail_server = self.env['fetchmail.server'].create({
            'name': 'Test server',
            'use_microsoft_outlook_service': True,
            'user': 'test@example.com',
            'microsoft_outlook_access_token': 'test_access_token',
            'microsoft_outlook_access_token_expiration': time.time() + 1000000,
            'password': '',
            'type': 'imap',
            'is_ssl': True,
        })

        mail_server.connect()

        mock_connection.authenticate.assert_called_once_with('XOAUTH2', ANY)
        args = mock_connection.authenticate.call_args[0]

        self.assertEqual(args[1](None), 'user=test@example.com\1auth=Bearer test_access_token\1\1',
                         msg='Should use the right access token')

        mock_connection.select.assert_called_once_with('INBOX')

    def test_constraints(self):
        """Test the constraints related to the Outlook mail server."""
        with self.assertRaises(ValidationError, msg='Should ensure that the password is empty'):
            self.env['fetchmail.server'].create({
                'name': 'Test server',
                'use_microsoft_outlook_service': True,
                'password': 'test',
                'type': 'imap',
            })

        with self.assertRaises(ValidationError, msg='Should ensure that the server type is IMAP'):
            self.env['fetchmail.server'].create({
                'name': 'Test server',
                'use_microsoft_outlook_service': True,
                'password': '',
                'type': 'pop',
            })
