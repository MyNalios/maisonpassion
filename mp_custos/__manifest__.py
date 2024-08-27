# -*- coding: utf-8 -*-
{
    'name': "mp_custos",

    'summary': """
        Customization for Maison Passion""",

    'description': """
        Customization for Maison Passion
    """,

    'author': "Nalios",
    'website': "https://www.nalios.be",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '17.0.1',

    # any module necessary for this one to work correctly
    'depends': ['crm', 'sale', 'mp_sale_layout', 'account'],

    # always loaded
    'data': [
        'views/account_payment_term_views.xml',
        'views/sale_order_views.xml',
        'views/crm_lead_views.xml',
        'report/invoice_report.xml',
    ],
}
