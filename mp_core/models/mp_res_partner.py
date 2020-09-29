# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MaisonPassionResPartner(models.Model):
    _inherit = 'res.partner'

    def _default_country_id(self):
        return self.env.company.country_id

    mobile = fields.Char(string='Mobile 1')
    mobile_2 = fields.Char(string='Mobile 2')
    is_client_effective = fields.Boolean(string='Effective Client', compute='_compute_is_client_effective',
                                         readonly=True)
    source_id = fields.Many2one('utm.source', string='Source', required=True)
    country_id = fields.Many2one('res.country', default=_default_country_id)
    is_red_code = fields.Boolean(string='Is a Red Code')

    @api.depends('sale_order_ids')
    def _compute_is_client_effective(self):
        for partner in self:
            if partner.sale_order_ids:
                partner.is_client_effective = True
            else:
                partner.is_client_effective = False

    @api.constrains('vat')
    def _check_unique_vat(self):
        for partner in self:
            if partner.company_type == 'person':
                continue
            result = self.search([('id', '!=', partner.id), ('vat', '!=', ""), ('vat', '=', partner.vat)], limit=1)
            if result:
                message = _('You have already defined a partner ({}) with this VAT number ({})'.format(result.name,
                                                                                                       partner.vat))
                raise ValidationError(message)

    @api.onchange('mobile_2', 'country_id', 'company_id')
    def _onchange_mobile_2_validation(self):
        if self.mobile_2:
            self.mobile_2 = self.phone_format(self.mobile_2)

    def write(self, vals):
        """
        If a child partner becomes independent, then a new sequence is created
        :param vals: values to update
        :return: super behavior
        """
        if self.parent_id:
            if not vals.get('parent_id', True):
                sequence = self.env['ir.sequence'].next_by_code("res.partner")
                vals.update({'ref': sequence})
        return super(MaisonPassionResPartner, self).write(vals)

    @api.model_create_multi
    def create(self, vals):
        """
        If contact has no parent then a new sequence is created
        :param vals: values to create
        :return: super behavior
        """
        for contact_vals in vals:
            if not contact_vals.get('parent_id') and not contact_vals.get('ref'):
                sequence = self.env['ir.sequence'].next_by_code("res.partner")
                contact_vals.update({'ref': sequence})
        res = super(MaisonPassionResPartner, self).create(vals)
        return res

    @api.model
    def _commercial_fields(self):
        """ Overriden method
        :return a list of fields which are synchronized between parent and children contacts """
        return super(MaisonPassionResPartner, self)._commercial_fields() + ['ref']

    @api.model
    def cron_format_phone_number(self):
        partner_ids = self.env['res.partner'].search(['|', '|', ('phone', '!=', False), ('mobile', '!=', False),
                                                      ('mobile_2', '!=', False)])
        self.action_format_phone_number(partner_ids.ids)

    @api.model
    def action_format_phone_number(self, partner_ids):
        partners = self.env['res.partner'].browse(partner_ids)
        for partner in partners:
            partner.phone = self.phone_format(partner.phone if partner.phone else "")
            partner.mobile = self.phone_format(partner.mobile if partner.mobile else "")
            partner.mobile_2 = self.phone_format(partner.mobile_2 if partner.mobile_2 else "")

