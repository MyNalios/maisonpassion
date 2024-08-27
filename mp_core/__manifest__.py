{
    'name': "Maison Passion Core",
    'version': '17.0',
    'category': 'All',
    'summary': 'Add Logic in the different models of Odoo in order to correspond with the way of working of the Maison Passion company.',
    'author': 'Idealis Consulting',
    'website': 'http://www.idealisconsulting.com',
    'depends': ['contacts', 'sale_management', 'crm', 'phone_validation'],
    'price': 0,
    'currency': 'EUR',
    'data': [
         'data/delete_module.sql',
         'data/mp_ref_partner_sequence.xml',
         'data/mp_phone_format_cron.xml',
         'data/res_partner_data.xml',
         'views/mp_res_partner_view.xml',
         'views/mp_sale_order_view.xml',
         'views/ir_qweb_widget_templates.xml'
    ],

    'installable': True,
}
