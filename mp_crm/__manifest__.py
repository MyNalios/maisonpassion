# -*- coding: utf-8 -*-
{
    'name': 'Maison Passion CRM',
    'version': '16.0',
    'category': 'Sales/CRM',
    'summary': '',
    'author': 'dwa@idealisconsulting - Idealis Consulting',
    'website': 'http://www.idealisconsulting.com',
    'depends': ['mp_core', 'crm', 'sales_team'],
    'data': [
        'views/crm_lead_views.xml',
        'views/res_partner_views.xml',
        'views/utm_source_views.xml',
        'wizard/crm_lead_to_opportunity_views.xml',
        'security/ir.model.access.csv',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
