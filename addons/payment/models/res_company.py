# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

from eagle import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    payment_acquirer_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), ('done', "Done")], string="State of the onboarding payment acquirer step", default='not_done')
    # YTI FIXME: Check if it's really needed on the company. Should be enough on the wizard
    payment_onboarding_payment_method = fields.Selection([
        ('paypal', "PayPal"),
        ('stripe', "Stripe"),
        ('manual', "Manual"),
        ('other', "Other"),
    ], string="Selected onboarding payment method")

    @api.model
    def action_open_payment_onboarding_payment_acquirer(self):
        """ Called by onboarding panel above the customer invoice list."""
        # Fail if there are no existing accounts
        self.env.user.company_id.get_chart_of_accounts_or_fail()

        action = self.env.ref('payment.action_open_payment_onboarding_payment_acquirer_wizard').read()[0]
        return action

    def get_account_invoice_onboarding_steps_states_names(self):
        """ Override. """
        steps = super(ResCompany, self).get_account_invoice_onboarding_steps_states_names()
        return steps + ['payment_acquirer_onboarding_state']
