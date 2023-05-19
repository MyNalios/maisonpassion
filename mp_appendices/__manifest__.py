# -*- coding: utf-8 -*-

{
    'name': "Maison Passion Portal Appendices",
    'version': '16.0',
    'category': 'Operations/Helpdesk',
    'summary': 'Add Technical Documents for Partners to Portal',
    'sequence': 90,
    'author': 'dwa@idealisconsulting - Idealis Consulting',
    'website': 'http://www.idealisconsulting.com',
    'depends': ['portal', 'mp_core'],
    'data': [
         'views/sale_technical_document_tag_views.xml',
         'views/sale_technical_document_templates.xml',
         'views/sale_technical_document_views.xml',
         'wizard/manage_technical_document_views.xml',
         'views/res_partner_views.xml',
         'security/ir.model.access.csv',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
