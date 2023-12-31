# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.
# Copyright (C) 2004-2008 PC Solutions (<http://pcsol.be>). All Rights Reserved
from eagle import fields, models, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    journal_user = fields.Boolean('Use in Point of Sale',
        help="Check this box if this journal define a payment method that can be used in a point of sale.")
    amount_authorized_diff = fields.Float('Amount Authorized Difference',
        help="This field depicts the maximum difference allowed between the ending balance and the theoretical cash when "
             "closing a session, for non-POS managers. If this maximum is reached, the user will have an error message at "
             "the closing of his session saying that he needs to contact his manager.")

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        session_id = self.env.context.get('pos_session_id', False)
        if session_id:
            session = self.env['pos.session'].browse(session_id)
            if session:
                args += [('id', 'in', session.config_id.journal_ids.ids)]
        return super(AccountJournal, self)._search(args=args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)

    @api.onchange('type')
    def onchange_type(self):
        if self.type not in ['bank', 'cash']:
            self.journal_user = False
