# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

from eagle import http
from eagle.http import request
from eagle.addons.website_form.controllers.main import WebsiteForm

class WebsiteForm(WebsiteForm):

    # Check and insert values from the form on the model <model>
    @http.route('/website_form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True)
    def website_form(self, model_name, **kwargs):
        if model_name == 'crm.lead' and not request.params.get('state_id'):
            geoip_country_code = request.session.get('geoip', {}).get('country_code')
            geoip_state_code = request.session.get('geoip', {}).get('region')
            if geoip_country_code and geoip_state_code:
                state = request.env['res.country.state'].search([('code', '=', geoip_state_code), ('country_id.code', '=', geoip_country_code)])
                if state:
                    request.params['state_id'] = state.id
        return super(WebsiteForm, self).website_form(model_name, **kwargs)

    def insert_record(self, request, model, values, custom, meta=None):
        if model.model == 'crm.lead':
            if 'company_id' not in values:
                values['company_id'] = request.website.company_id.id
        return super(WebsiteForm, self).insert_record(request, model, values, custom, meta=meta)
