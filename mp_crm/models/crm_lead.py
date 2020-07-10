# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Lead(models.Model):
    _inherit = 'crm.lead'

    mobile = fields.Char(string='Mobile 1')
    mobile_2 = fields.Char(string='Mobile 2')
    referred_partner_ids = fields.Many2many('res.partner', 'crm_referred_partner_rel', 'lead_id', 'partner_id', string='Referred By')

    def write(self, vals):
        if self.type == 'lead':
            vals.update(self._get_partner_vals_from_email(vals.get('email_from')))  # overwrite existing keys
        return super(Lead, self).write(vals)

    @api.model
    def create(self, vals):
        if vals.get('type') == 'lead':
            vals.update(self._get_partner_vals_from_email(vals.get('email_from')))  # overwrite existing keys
        return super(Lead, self).create(vals)

    def _get_partner_vals_from_email(self, email):
        if email:
            partner = self.env['res.partner'].search([('email', '=', email)])
            if partner:
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



