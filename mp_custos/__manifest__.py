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
    'category': 'Maison Passion',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['crm','sale','mp_sale_layout','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/crm_lead_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
