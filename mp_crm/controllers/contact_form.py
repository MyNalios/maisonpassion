# -*- coding: utf-8 -*-
import json
import re
from werkzeug.wrappers import Response
from odoo import http, tools, _
from odoo.http import request
from odoo.addons.phone_validation.tools import phone_validation


class ContactForm(http.Controller):

    @http.route('/contact_json', type='json', auth='public', csrf=False, methods=['POST'])
    def create_lead_from_json(self, **post):
        try:
            data = json.loads(request.httprequest.data)
            # logging request
            vals = {
                'url': request.httprequest.url or '',
                'charset': request.httprequest.charset or '',
                'content_type': request.httprequest.content_type or '',
                'mimetype': request.httprequest.mimetype or '',
                'method': request.httprequest.method or '',
                'form_data': ', '.join(['{}:{}'.format(k, v) for k, v in data.items()])
            }
            request.env['crm.lead.creation.log'].sudo().create(vals)
            return json.dumps({'success': True})
        except Exception:
            return Response("Wrong content", status=400)

    @http.route('/contact', type='http', auth='public', csrf=False, methods=['POST'])
    def create_lead_from_http(self, **post):
        # logging request
        vals = {
            'url': request.httprequest.url or '',
            'charset': request.httprequest.charset or '',
            'content_type': request.httprequest.content_type or '',
            'mimetype': request.httprequest.mimetype or '',
            'method': request.httprequest.method or '',
            'params': ', '.join(['{}:{}'.format(k, v) for k, v in request.params.items()]),
            'form_data': ', '.join(['{}:{}'.format(k, v) for k, v in request.httprequest.form.items()])
        }
        request.env['crm.lead.creation.log'].sudo().create(vals)

        if post.get('source') == 'Bobex' and (post.get('your-tel') or post.get('your-email')) and post.get('your-name'):
            tag_ids = []
            if 'services[]' in post:
                formatted_services = re.sub('\s*,\s*', ',', post['services[]'])
                tag_names = formatted_services.split(',')
                for tag_name in tag_names:
                    tag = request.env['crm.lead.tag'].sudo().search([('technical_name', '=', tag_name)], limit=1)
                    if tag:
                        tag_ids.append(tag.id)

            formatted_name = ' '.join([x for x in (post.get('your-name', ''), post.get('your-firstname', '')) if x != ''])
            vals = {
                'name': '[Bobex] {}'.format(formatted_name),
                'type': 'lead',
                'country_id': request.env['res.country'].search([('code', '=', 'BE')]).id or False,
                'lang_id': request.env['res.lang'].search([('code', '=', post.get('your-lang'))]).id if post.get('your-lang') else request.env['res.lang'].search([('code', '=', 'fr_BE')]).id or False,
                'contact_name': formatted_name,
                'email_from': tools.formataddr((formatted_name, post.get('your-email'))) if post.get('your-email') else '',
                'phone': phone_validation.phone_format(post.get('your-tel'), 'BE', '32', force_format='INTERNATIONAL', raise_exception=False) or '',
                'street': post.get('your-adres', ''),
                'city': post.get('your-local', ''),
                'zip': post.get('your-postal', ''),
                'description': _('Bobex Reference: {}\n{}').format(post.get('sourceref', ''), post.get('your-message', '')),
                'source_id': request.env['utm.source'].sudo().search([('technical_name', '=', 'bobex')]).id or False,
                'tag_ids': [(6, 0, tag_ids)]
            }
            request.env['crm.lead'].sudo().create(vals)
            return 'OK'

        elif post.get('source') == 'website' and post.get('demande') == 'Demande de devis gratuit' and (post.get('tel') or post.get('email')) and post.get('name'):
            tag_ids = []
            if 'services' in post:
                formatted_services = re.sub('\s*,\s*', ',', post['services'])
                tag_names = formatted_services.split(',')
                for tag_name in tag_names:
                    tag = request.env['crm.lead.tag'].sudo().search([('technical_name', '=', tag_name)])
                    if tag:
                        tag_ids.append(tag.id)

            vals = {
                'name': '{} - {}'.format(post.get('services', ''), post['name']) if post.get('services') else post['name'],
                'type': 'lead',
                'country_id': request.env['res.country'].search([('code', '=', 'BE')]).id or False,
                'lang_id': request.env['res.lang'].search([('code', '=', 'fr_BE')]).id or False,
                'contact_name': post['name'],
                'email_from': tools.formataddr((post['name'], post.get('email'))) if post.get('email') else '',
                'phone': phone_validation.phone_format(post.get('tel'), 'BE', '32', force_format='INTERNATIONAL', raise_exception=False) or '',
                'street': post.get('adres', ''),
                'city': post.get('local', ''),
                'zip': post.get('postal', ''),
                'description': '{}\n{}'.format('Demande de devis gratuit:', post.get('message', '')),
                'source_id': request.env['utm.source'].sudo().search([('technical_name', '=', 'website')]).id or False,
                'tag_ids': [(6, 0, tag_ids)]
            }
            request.env['crm.lead'].sudo().create(vals)
            return 'OK'

        elif post.get('secret') and (post.get('phone') or post.get('email')) and post.get('last_name'):
            try:
                data_list = request.httprequest.form.getlist('additional_data')
                data = '\n'.join(data_list)
            except Exception:
                data = post.get('additional_data', '')

            try:
                product_list = request.httprequest.form.getlist('products')
                products = '\n'.join(product_list)
            except Exception:
                products = post.get('products', '')

            formatted_name = ' '.join([x for x in (post.get('last_name', ''), post.get('first_name', '')) if x != ''])
            vals = {
                'name': '[Solvari] {}'.format(formatted_name),
                'type': 'lead',
                'country_id': request.env['res.country'].search([('code', '=', 'BE')]).id or False,
                'lang_id': request.env['res.lang'].search([('code', '=', 'fr_BE')]).id or False,
                'contact_name': formatted_name,
                'email_from': tools.formataddr((post['last_name'], post.get('email'))) if post.get('email') else '',
                'phone': phone_validation.phone_format(post.get('phone'), 'BE', '32', force_format='INTERNATIONAL', raise_exception=False) or '',
                'street': ', '.join([x for x in (post.get('street', ''), post.get('house_nr', '')) if x != '']),
                'city': post.get('city', ''),
                'zip': post.get('zip_code', ''),
                'description': '{}{}{}{}{}'.format(
                    _('Message By Solvari: {}\n').format(post.get('message_by_solvari')) if post.get('message_by_solvari') else '',
                    _('Amount of Competitors: {}\n').format(post.get('competitors')) if post.get('competitors') else '',
                    _('Description: {}\n').format(post.get('description')) if post.get('description') else '',
                    _('Questions: {}\n').format(data),
                    _('Products: {}\n').format(products)),
                'source_id': request.env['utm.source'].sudo().search([('technical_name', '=', 'solvari')]).id or False,
            }
            request.env['crm.lead'].sudo().create(vals)
            return json.dumps({'success': True})

        else:
            return Response("Wrong parameters", status=400)
