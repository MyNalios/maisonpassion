{
    'name': "Maison Passion Invoice Layout",
    'version': '15.0',
    'category': 'Accounting/Accounting',
    'summary': 'Modifications to Invoices layout',
    'author': 'dwa@idealisconsulting - Idealis Consulting',
    'website': 'http://www.idealisconsulting.com',
    'depends': ['account', 'mp_core'],
    'data': [
        'report/account_move_templates.xml',
        'views/account_move_views.xml',
        'views/sale_advance_payment_inv_views.xml',
        'views/account_tax_from_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
