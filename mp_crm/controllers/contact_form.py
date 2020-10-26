# -*- coding: utf-8 -*-

from odoo import http, tools
from odoo.http import request
from odoo.addons.phone_validation.tools import phone_validation


class ContactForm(http.Controller):

    @http.route('/contact', type='http', auth='public', csrf=False, methods=['POST'])
    def create_lead(self, **post):
        if post.get('source') == 'Bobex' and (post.get('your-tel') or post.get('your-email')) and post.get('your-name'):
            vals = {
                'name': '{} - {} {}'.format(post['source'], post['your-name'], post.get('your-firstname', '')),
                'type': 'lead',
                'country_id': request.env['res.country'].search([('code', '=', 'BE')]).id or False,
                'lang_id': request.env['res.lang'].search([('code', '=', post.get('your-lang'))]).id if post.get('your-lang') else request.env['res.lang'].search([('code', '=', 'fr_BE')]).id or False,
                'contact_name': '{} {}'.format(post['your-name'], post.get('your-firstname', '')),
                'email_from': tools.formataddr(
                    (post['your-name'] or u"False", post.get('your-email') or u"False")) if post.get(
                    'your-email') else '',
                'phone': phone_validation.phone_format(post.get('your-tel'), 'BE', '32', force_format='INTERNATIONAL',
                                                       raise_exception=False) or '',
                'street': post.get('your-adres') or '',
                'city': post.get('your-local') or '',
                'zip': post.get('your-postal') or '',
                'description': post.get('your-message') or '',
                'source_id': request.env['utm.source'].sudo().search([('technical_name', '=', 'bobex')]).id or False,
            }
            request.env['crm.lead'].sudo().create(vals)
            return 'OK'

        elif post.get('menu-demande') == 'Demande de devis gratuit' and (post.get('your-tel') or post.get('your-email')) and post.get('your-name'):
            tags = request.httprequest.form.getlist('services[]')
            tag_ids = []
            for tag in tags:
                tag_id = request.env['crm.lead.tag'].sudo().search([('technical_name', '=', tag)])
                if tag_id:
                    tag_ids.append(tag_id.id)
            vals = {
                'name': '{} - {}'.format(' ,'.join(tags), post['your-name']),
                'type': 'lead',
                'country_id': request.env['res.country'].search([('code', '=', 'BE')]).id or False,
                'lang_id': request.env['res.lang'].search([('code', '=', 'fr_BE')]).id or False,
                'contact_name': post['your-name'],
                'email_from': tools.formataddr((post['your-name'] or u"False", post.get('your-email') or u"False")) if post.get('your-email') else '',
                'phone': phone_validation.phone_format(post.get('your-tel'), 'BE', '32', force_format='INTERNATIONAL', raise_exception=False) or '',
                'street': post.get('your-adres') or '',
                'city': post.get('your-local') or '',
                'zip': post.get('your-postal') or '',
                'description': post.get('your-message') or '',
                'source_id': request.env['utm.source'].sudo().search([('technical_name', '=', 'website')]).id or False,
                'tag_ids': [(6, 0, tag_ids)]
            }
            request.env['crm.lead'].sudo().create(vals)
            return 'OK'
        return 'NOK'

