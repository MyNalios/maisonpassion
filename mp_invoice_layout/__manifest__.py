# -*- coding: utf-8 -*-

{
    'name': "Maison Passion Invoice Layout",
    'version': '13.0.0.1',
    'category': 'Accounting/Accounting',
    'summary': 'Modifications to Invoices layout',
    'author': 'dwa@idealisconsulting - Idealis Consulting',
    'website': 'http://www.idealisconsulting.com',
    'depends': ['account', 'sale'],
    'data': [
        'report/account_move_templates.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
