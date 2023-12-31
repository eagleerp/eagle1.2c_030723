# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.
from eagle.addons.web_editor.controllers.main import Web_Editor
from eagle.http import request


class Web_Editor(Web_Editor):

    def _get_view_fields_to_read(self):
        res = super(Web_Editor, self)._get_view_fields_to_read()
        res.append('website_id')
        return res

    def save_scss_view_hook(self):
        res = super(Web_Editor, self).save_scss_view_hook()

        website = request.env['website'].get_current_website()
        if website:
            res['website_id'] = website.id
        return res

    def save_scss_attachment_hook(self):
        res = super(Web_Editor, self).save_scss_attachment_hook()

        website = request.env['website'].get_current_website()
        if website:
            res['website_id'] = website.id
        return res

    def get_custom_attachment(self, custom_url, op='='):
        website = request.env['website'].get_current_website()
        res = super(Web_Editor, self).get_custom_attachment(custom_url, op=op)
        return res.with_context(website_id=website.id).filtered(lambda x: not x.website_id or x.website_id == website)

    def get_custom_view(self, custom_url, op='='):
        website = request.env['website'].get_current_website()
        res = super(Web_Editor, self).get_custom_view(custom_url, op=op)
        return res.with_context(website_id=website.id).filter_duplicate()
