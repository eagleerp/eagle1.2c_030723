# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

from eagle import api, fields, models


class Company(models.Model):
    _inherit = "res.company"

    social_twitter = fields.Char('Twitter Account')
    social_facebook = fields.Char('Facebook Account')
    social_github = fields.Char('GitHub Account')
    social_linkedin = fields.Char('LinkedIn Account')
    social_youtube = fields.Char('Youtube Account')
    social_googleplus = fields.Char('Google+ Account')
    social_instagram = fields.Char('Instagram Account')
