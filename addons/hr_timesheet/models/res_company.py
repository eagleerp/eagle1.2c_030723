# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

from eagle import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.model
    def _default_project_time_mode_id(self):
        uom = self.env.ref('uom.product_uom_hour', raise_if_not_found=False)
        if not uom:
            uom = self.env['uom.uom'].search([('measure_type', '=', 'time'), ('uom_type', '=', 'reference')], limit=1)
        if not uom:
            uom = self.env['uom.uom'].search([('measure_type', '=', 'time')], limit=1)
        return uom

    @api.model
    def _default_timesheet_encode_uom_id(self):
        uom = self.env.ref('uom.product_uom_hour', raise_if_not_found=False)
        if not uom:
            uom = self.env['uom.uom'].search([('measure_type', '=', 'time'), ('uom_type', '=', 'reference')], limit=1)
        if not uom:
            uom = self.env['uom.uom'].search([('measure_type', '=', 'time')], limit=1)
        return uom

    project_time_mode_id = fields.Many2one('uom.uom', string='Project Time Unit',
        default=_default_project_time_mode_id, domain=[('measure_type', '=', 'time')],
        help="This will set the unit of measure used in projects and tasks.\n"
             "If you use the timesheet linked to projects, don't "
             "forget to setup the right unit of measure in your employees.")
    timesheet_encode_uom_id = fields.Many2one('uom.uom', string="Timesheet Encoding Unit",
        default=_default_timesheet_encode_uom_id, domain=[('measure_type', '=', 'time')], required=True,
        help="""This will set the unit of measure used to encode timesheet. This will simply provide tools
        and widgets to help the encoding. All reporting will still be expressed in hours (default value).""")
