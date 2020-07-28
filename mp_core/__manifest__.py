# -*- coding: utf-8 -*-

{
    'name': "Maison Passion Core",
    'version': '13.0.0.1',
    'category': 'All',
    'summary': 'Add Logic in the different models of Odoo in order to correspond with the way of working of the Maison Passion company.',
    'author': 'Idealis Consulting',
    'website': 'http://www.idealisconsulting.com',
    'depends': ['base', 'contacts', 'sale_management', 'crm'],
    'price': 0,
    'currency': 'EUR',
    'data': [
        'data/mp_ref_partner_sequence.xml',
        'views/mp_res_partner_view.xml',
        'views/mp_sale_order_view.xml',
        'views/ir_qweb_widget_templates.xml'
    ],

    'installable': True,
}