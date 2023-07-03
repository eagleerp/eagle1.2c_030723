# -*- coding: utf-8 -*-

from eagle import fields, models, _

from eagle.tools.float_utils import float_is_zero

from eagle.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    stock_move_id = fields.Many2one('stock.move', string='Stock Move')
