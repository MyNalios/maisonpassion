# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Lead(models.Model):
    _inherit = 'crm.lead'

    mobile = fields.Char(string='Mobile 1')
    mobile_2 = fields.Char(string='Mobile 2')
    referred_partner_id = fields.Many2one('res.partner', string='Referred By', domain=[('type', '=', 'contact')])
    address_type = fields.Selection(
        [('contact', 'Contact'),
         ('invoice', 'Invoice Address'),
         ('delivery', 'Delivery Address'),
         ('other', 'Other Address'),
         ("private", "Private Address"),
         ], string='Address Type',
        default='contact',
        help="Invoice & Delivery addresses are used in sales orders. Private addresses are only visible by authorized users.")
    vat = fields.Char(string='Tax ID', help="The Tax Identification Number. Complete it if the contact is subjected to government taxes. Used in some legal statements.")

    def write(self, vals):
        if (vals.get('type') == 'lead' or self.type == 'lead') \
                and (vals.get('email_from') or vals.get('phone') or vals.get('mobile')) \
                and not self.env.context.get('no_contact_synchronization'):
            vals.update(self._get_partner_vals_from_email(vals.get('email_from'), vals.get('phone'), vals.get('mobile')))  # overwrite existing keys
        return super(Lead, self).write(vals)

    @api.model
    def create(self, vals):
        if vals.get('type') == 'lead' \
                and (vals.get('email_from') or vals.get('phone') or vals.get('mobile')) \
                and not self.env.context.get('no_contact_synchronization'):
            vals.update(self._get_partner_vals_from_email(vals.get('email_from'), vals.get('phone'), vals.get('mobile')))  # overwrite existing keys
        return super(Lead, self).create(vals)

    def _get_partner_vals_from_email(self, email=None, phone=None, mobile=None):
        domain = []
        if email or self.email_from:
            domain.append(('email', '=', email or self.email_from))
        if phone or self.phone:
            domain.append(('phone', '=', phone or self.phone))
        if mobile or self.mobile:
            domain.append(('mobile', '=', mobile or self.phone))
        if domain:
            partner = self.env['res.partner'].search(domain)
            if len(partner) == 1:
                onchange_values = self._onchange_partner_id_values(partner.id)
                onchange_values.update({
                    'partner_id': partner.id,
                    'mobile': partner.mobile,
                    'mobile_2': partner.mobile_2,
                    'website': partner.website,
                    'source_id': partner.source_id.id or False,
                    'address_type': partner.type,
                    'vat': partner.vat,
                    'referred_partner_id': partner.referred_partner_id.id or False,
                    'lang_id': self.env['res.lang'].search([('code', '=', partner.lang)]).id or False
                })
                return onchange_values
        return {}

    def action_new_quotation(self):
        action = super(Lead, self).action_new_quotation()
        action['context'].update({'default_user_id': self.user_id.id})
        return action

    def _create_lead_partner_data(self, name, is_company, parent_id=False):
        res = super(Lead, self)._create_lead_partner_data(name, is_company, parent_id)
        res.update({'type': self.address_type, 'vat': self.vat, 'referred_partner_id': self.referred_partner_id.id or False, 'mobile_2': self.mobile_2, 'source_id': self.source_id.id or False})
        return res
