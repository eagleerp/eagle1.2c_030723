# -*- encoding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

{
    'name': 'Recruitment',
    'version': '1.0',
    'category': 'Human Resources',
    'sequence': 90,
    'summary': 'Track your recruitment pipeline',
    'description': "",
    'website': 'https://www.eagle-erp.com/page/recruitment',
    'depends': [
        'hr',
        'calendar',
        'fetchmail',
        'utm',
        'document',
        'web_tour',
        'digest',
    ],
    'data': [
        'security/hr_recruitment_security.xml',
        'security/ir.model.access.csv',
        'data/hr_recruitment_data.xml',
        'data/digest_data.xml',
        'views/hr_recruitment_views.xml',
        'views/res_config_settings_views.xml',
        'views/hr_recruitment_templates.xml',
        'views/hr_department_views.xml',
        'views/hr_job_views.xml',
        'views/mail_activity_views.xml',
        'views/digest_views.xml',
    ],
    'demo': [
        'data/hr_recruitment_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
