# -*- coding: utf-8 -*-

{
    'name': "Maison Passion Portal Appendices",
    'version': '13.0.0.1',
    'category': 'Operations/Helpdesk',
    'summary': 'Add Technical Documents for Users to Portal',
    'sequence': 90,
    'author': 'dwa@idealisconsulting - Idealis Consulting',
    'website': 'http://www.idealisconsulting.com',
    'depends': ['portal'],
    'data': [
        'views/sale_technical_document_tag_views.xml',
        'views/sale_technical_document_templates.xml',
        'views/sale_technical_document_views.xml',
        'wizard/manage_technical_document_views.xml',
        'views/res_users_views.xml',
        'security/ir.model.access.csv',
        'data/document_demo.xml'
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
