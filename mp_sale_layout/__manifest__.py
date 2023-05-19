# -*- coding: utf-8 -*-

{
    'name': "Maison Passion Sale Layout",
    'version': '16.0',
    'category': 'Sales/Sales',
    'summary': 'Modifications to Sales Orders layout',
    'author': 'dwa@idealisconsulting - Idealis Consulting',
    'website': 'http://www.idealisconsulting.com',
    'depends': ['mp_core', 'web'],
    'data': [
         'report/sale_order_templates.xml',
         'views/sale_order_views.xml',
         'views/sale_order_templates.xml',
         'report/external_layout_templates.xml',
    ],
     'assets': {
        'web.assets_backend': [
            # 'mp_sale_layout/static/src/js/section_and_note.js',
            # 'mp_sale_layout/static/src/scss/section_and_note.scss',
        ],
    },
    'installable': True,
    'auto_install': False,
}
