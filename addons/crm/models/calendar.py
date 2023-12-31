# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

from eagle import api, fields, models


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    def _is_crm_lead(self, defaults, ctx=None):
        """
            This method checks if the concerned model is a CRM lead.
            The information is not always in the defaults values,
            this is why it is necessary to check the context too.
        """
        res_model = defaults.get('res_model', False) or ctx and ctx.get('default_res_model')
        res_model_id = defaults.get('res_model_id', False) or ctx and ctx.get('default_res_model_id')

        return res_model and res_model == 'crm.lead' or res_model_id and self.env['ir.model'].sudo().browse(res_model_id).model == 'crm.lead'

    @api.model
    def default_get(self, fields):
        if self.env.context.get('default_opportunity_id'):
            self = self.with_context(
                default_res_model_id=self.env.ref('crm.model_crm_lead').id,
                default_res_id=self.env.context['default_opportunity_id']
            )
        defaults = super(CalendarEvent, self).default_get(fields)

        # sync res_model / res_id to opportunity id (aka creating meeting from lead chatter)
        ctx = self.env.context
        if 'opportunity_id' not in defaults:
            if self._is_crm_lead(defaults, ctx):
                defaults['opportunity_id'] = defaults.get('res_id', False) or ctx.get('default_res_id', False)

        return defaults

    def _compute_is_highlighted(self):
        super(CalendarEvent, self)._compute_is_highlighted()
        if self.env.context.get('active_model') == 'crm.lead':
            opportunity_id = self.env.context.get('active_id')
            for event in self:
                if event.opportunity_id.id == opportunity_id:
                    event.is_highlighted = True

    opportunity_id = fields.Many2one('crm.lead', 'Opportunity', domain="[('type', '=', 'opportunity')]")

    @api.model
    def create(self, vals):
        event = super(CalendarEvent, self).create(vals)

        if event.opportunity_id and not event.activity_ids:
            event.opportunity_id.log_meeting(event.name, event.start, event.duration)
        return event
