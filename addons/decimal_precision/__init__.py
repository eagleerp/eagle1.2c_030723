# -*- encoding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.
from eagle import api, SUPERUSER_ID

from . import models

def get_precision(application):
    def change_digit(cr):
        env = api.Environment(cr, SUPERUSER_ID, {})
        precision = env['decimal.precision'].precision_get(application)
        return 16, precision

    return change_digit
