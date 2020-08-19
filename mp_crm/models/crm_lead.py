# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Lead(models.Model):
    _inherit = 'crm.lead'

    mobile = fields.Char(string='Mobile 1')
    mobile_2 = fields.Char(string='Mobile 2')
    referred_partner_ids = fields.Many2many('res.partner', 'crm_referred_partner_rel', 'lead_id', 'partner_id', string='Referred By')

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
                    'mobile': partner.mobile or False,
                    'mobile_2': partner.mobile_2 or False,
                    'website': partner.website or False,
                    'source_id': partner.source_id.id or False,
                    'lang_id': self.env['res.lang'].search([('code', '=', partner.lang)]).id or False
                })
                return onchange_values
        return {}



