# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

from eagle.addons.survey.controllers.main import Survey
from eagle.http import request


class WebsiteSurvey(Survey):

    def _print_survey(self, survey, token=None):
        if survey.auth_required and request.env.user == request.website.user_id:
            return request.render("survey.auth_required", {'survey': survey, 'token': token})
        return super()._print_survey(survey, token)
