# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.
import re
from collections import OrderedDict

from eagle import models
from eagle.addons.http_routing.models.ir_http import url_for
from eagle.osv import expression
from eagle.http import request
from eagle.addons.base.models.assetsbundle import AssetsBundle
from eagle.tools import html_escape as escape

re_background_image = re.compile(r"(background-image\s*:\s*url\(\s*['\"]?\s*)([^)'\"]+)")


class AssetsBundleMultiWebsite(AssetsBundle):
    def _get_asset_url_values(self, id, unique, extra, name, page, type):
        website_id = self.env.context.get('website_id')
        website_id_path = website_id and ('%s/' % website_id) or ''
        extra = website_id_path + extra
        res = super(AssetsBundleMultiWebsite, self)._get_asset_url_values(id, unique, extra, name, page, type)
        return res

    def _get_assets_domain_for_already_processed_css(self, assets):
        res = super(AssetsBundleMultiWebsite, self)._get_assets_domain_for_already_processed_css(assets)
        current_website = self.env['website'].get_current_website(fallback=False)
        res = expression.AND([res, current_website.website_domain()])
        return res

class QWeb(models.AbstractModel):
    """ QWeb object for rendering stuff in the website context """

    _inherit = 'ir.qweb'

    URL_ATTRS = {
        'form':   'action',
        'a':      'href',
        'link':   'href',
        'script': 'src',
        'img':    'src',
    }

    def get_asset_bundle(self, xmlid, files, remains=None, env=None):
        return AssetsBundleMultiWebsite(xmlid, files, remains=remains, env=env)

    def _post_processing_att(self, tagName, atts, options):
        if atts.get('data-no-post-process'):
            return atts

        atts = super(QWeb, self)._post_processing_att(tagName, atts, options)

        if options.get('inherit_branding') or options.get('rendering_bundle') or \
           options.get('edit_translations') or options.get('debug') or (request and request.debug):
            return atts

        website = request and getattr(request, 'website', None)
        if not website and options.get('website_id'):
            website = self.env['website'].browse(options['website_id'])

        if not website:
            return atts

        name = self.URL_ATTRS.get(tagName)
        if request and name and name in atts:
            atts[name] = url_for(atts[name])

        if not website.cdn_activated:
            return atts

        if name and name in atts:
            atts = OrderedDict(atts)
            atts[name] = website.get_cdn_url(atts[name])
        if isinstance(atts.get('style'), str) and 'background-image' in atts['style']:
            atts = OrderedDict(atts)
            atts['style'] = re_background_image.sub(lambda m: '%s%s' % (m.group(1), website.get_cdn_url(m.group(2))), atts['style'])

        return atts
