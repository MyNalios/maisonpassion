# -*- coding: utf-8 -*-

{
    'name': "Maison Passion Sale Layout",
    'version': '13.0.0.1',
    'category': 'Sales/Sales',
    'summary': 'Modifications to Sales Orders layout',
    'author': 'dwa@idealisconsulting - Idealis Consulting',
    'website': 'http://www.idealisconsulting.com',
    'depends': ['mp_core', 'sale', 'web'],
    'data': [
        'report/sale_order_templates.xml',
        'views/sale_order_views.xml',
        'views/sale_order_templates.xml',
        'report/external_layout_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
}
