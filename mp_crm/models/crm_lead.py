# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Lead(models.Model):
    _inherit = 'crm.lead'

    def _default_country_id(self):
        return self.env.company.country_id

    def _default_lang_id(self):
        return self.env['res.lang'].search([('code', '=', self.env.lang)])

    def _default_title(self):
        return self.env.ref('mp_core.res_partner_title_mister_madam').id

    # default values
    country_id = fields.Many2one('res.country', default=_default_country_id)
    lang_id = fields.Many2one('res.lang', default=_default_lang_id)
    title = fields.Many2one('res.partner.title', default=_default_title)

    mobile = fields.Char(string='Mobile 1')
    mobile_2 = fields.Char(string='Mobile 2')
    referred_partner_id = fields.Many2one('res.partner', string='Referred By', domain=[('type', '=', 'contact')])
    address_type = fields.Selection(
        [('contact', 'Contact'),
         ('invoice', 'Invoice Address'),
         ('delivery', 'Delivery Address'),
         ('other', 'Other Address'),
         ('private', 'Private Address'),
         ], string='Address Type',
        default='contact',
        help='Invoice & Delivery addresses are used in sales orders. Private addresses are only visible by authorized users.')
    vat = fields.Char(string='Tax ID', help='The Tax Identification Number. Complete it if the contact is subjected to government taxes. Used in some legal statements.')

    def write(self, vals):
        # if (vals.get('type') == 'lead' or self.type == 'lead') \
        #         and (vals.get('email_from') or vals.get('phone') or vals.get('mobile')) \
        #         and not self.env.context.get('no_contact_synchronization'):
        #     vals.update(self._get_partner_vals_from_email(vals.get('email_from'), vals.get('phone'), vals.get('mobile')))  # overwrite existing ke               
        res = super().write(vals)
        for rec in self:
            if rec.partner_id:
                if rec.street:
                    rec.partner_id.street = rec.street
                if rec.street2:
                    rec.partner_id.street2 = rec.street2
                if rec.city:
                    rec.partner_id.city = rec.city
                if rec.state_id:
                    rec.partner_id.state_id = rec.state_id.id
                if rec.zip:
                    rec.partner_id.zip = rec.zip
                if rec.country_id:
                    rec.partner_id.country_id = rec.country_id.id
                if rec.mobile:
                    rec.partner_id.mobile = rec.mobile
                if rec.mobile_2:
                    rec.partner_id.mobile_2 = rec.mobile_2
                if rec.referred_partner_id:
                    rec.partner_id.referred_partner_id = rec.referred_partner_id.id
                if rec.source_id:
                    rec.partner_id.source_id = rec.source_id.id
        return res

    @api.onchange('mobile_2', 'country_id', 'company_id')
    def _onchange_mobile2_validation(self):
        if self.mobile_2:
            self.mobile_2 = self._phone_format(fname='mobile_2', force_format='INTERNATIONAL') or self.mobile_2

    @api.model
    def create(self, vals):
        # if vals.get('type') == 'lead' \
        #         and (vals.get('email_from') or vals.get('phone') or vals.get('mobile')) \
        #         and not self.env.context.get('no_contact_synchronization'):
        #     vals.update(self._get_partner_vals_from_email(vals.get('email_from'), vals.get('phone'), vals.get('mobile')))  # overwrite existing keys
        res = super().create(vals)
        for rec in self:
            if rec.partner_id:
                if rec.street:
                    rec.partner_id.street = vals['street']
                if rec.street2:
                    rec.partner_id.street2 = vals['street2']
                if rec.city:
                    rec.partner_id.city = vals['city']
                if rec.state_id:
                    rec.partner_id.state_id = vals['state_id']
                if rec.zip:
                    rec.partner_id.zip = vals['zip']
                if rec.country_id:
                    rec.partner_id.country_id = vals['country_id']
                if rec.mobile:
                    rec.partner_id.mobile = vals['mobile']
                if rec.mobile_2:
                    rec.partner_id.mobile_2 = vals['mobile_2']
                if rec.referred_partner_id:
                    rec.partner_id.referred_partner_id = vals['referred_partner_id']
                if rec.source_id:
                    rec.partner_id.source_id = vals['source_id']
        return res
    
    # def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
    #     res = super()._prepare_customer_values(partner_name, is_company,parent_id)
    #     dict_new_values = {
    #         'mobile_2': self.mobile_2,
    #         'referred_partner_id' : self.referred_partner_id.id,
    #         'source_id' : self.source_id.id
    #     }
    #     res.update(dict_new_values)
    #     return res

    # def _get_partner_vals_from_email(self, email=None, phone=None, mobile=None):
    #     domain = []
    #     if email or self.email_from:
    #         domain.append(('email', '=', email or self.email_from))
    #     if phone or self.phone:
    #         domain.append(('phone', '=', phone or self.phone))
    #     if mobile or self.mobile:
    #         domain.append(('mobile', '=', mobile or self.phone))
    #     if domain:
    #         partner = self.env['res.partner'].search(domain)
    #         # if there is more than one related partner, return none of them
    #         if len(partner) == 1:
    #             onchange_values = self._prepare_values_from_partner(partner)
    #             onchange_values.update({
    #                 'partner_id': partner.id,
    #                 'mobile': partner.mobile,
    #                 'mobile_2': partner.mobile_2,
    #                 'website': partner.website,
    #                 'source_id': partner.source_id.id or False,
    #                 'address_type': partner.type,
    #                 'vat': partner.vat,
    #                 'referred_partner_id': partner.referred_partner_id.id or False,
    #                 'lang_id': self.env['res.lang'].search([('code', '=', partner.lang)]).id or False
    #             })
    #             return onchange_values
    #     return {}

    # def action_new_quotation(self):
    #     action = super(Lead, self).action_new_quotation()
    #     action['context'].update({'default_user_id': self.user_id.id})
    #     return action

    # def _create_lead_partner_data(self, name, is_company, parent_id=False):
    #     res = super(Lead, self)._create_lead_partner_data(name, is_company, parent_id)
    #     res.update({'type': self.address_type, 'vat': self.vat, 'referred_partner_id': self.referred_partner_id.id or False, 'mobile_2': self.mobile_2, 'source_id': self.source_id.id or False})
    #     return res
