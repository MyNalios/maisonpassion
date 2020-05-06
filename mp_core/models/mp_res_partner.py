# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MaisonPassionResPartner(models.Model):
    _inherit = 'res.partner'

    mobile = fields.Char(string=_('Mobile Mr'))
    mobile_ms = fields.Char(string=_('Mobile Ms'))
    email_2 = fields.Char(string=_('Email 2'))
    is_client_effective = fields.Boolean(string=_('Effective Client'), compute='set_is_client_effective', readonly=True)
    source_ids = fields.Many2many('utm.source', 'partner_crm_source_rel', 'partner_id', 'source_id', string=_('Sources')
                                  , compute='set_source_ids', store=True)
    referred = fields.Char(string=_('Referred By'), compute='set_referred')

    @api.constrains('ref')
    def _check_unique_ref(self):
        for partner in self:
            if not partner.parent_id:
                result = self.search([('id', '!=', partner.id), ('id', 'not in', partner.child_ids.ids),
                                      ('ref', '!=', ""), ('ref', '=', partner.ref)], limit=1)
                if result:
                    message = _("You have already a partner ({}) with this reference ({})".format(result.name,
                                                                                                  partner.ref))
                    raise ValidationError(message)

    @api.constrains('vat')
    def _check_unique_vat(self):
        for partner in self:
            if partner.company_type == 'person':
                continue
            result = self.search([('id', '!=', partner.id), ('vat', '!=', ""), ('vat', '=', partner.vat)], limit=1)
            if result:
                message = _("You have already defined a partner ({}) with this VAT number ({})".format(result.name,
                                                                                                       partner.vat))
                raise ValidationError(message)

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
            if not contact_vals.get('parent_id'):
                sequence = self.env['ir.sequence'].next_by_code("res.partner")
                contact_vals.update({'ref': sequence})
        res = super(MaisonPassionResPartner, self).create(vals)
        return res

    @api.model
    def _commercial_fields(self):
        """ Overriden method
        :return a list of fields which are synchronized between parent and children contacts """
        return ['vat', 'credit_limit', 'ref']

    def set_is_client_effective(self):
        for partner in self:
            if self.env['sale.order'].search([('partner_id', '=', partner.id)]):
                partner.is_client_effective = True
            else:
                partner.is_client_effective = False

    def set_source_ids(self):
        for partner in self:
            lead_partner_ids = self.env['crm.lead'].search([('partner_id', '=', partner.id)])
            for lead in lead_partner_ids:
                if lead.source_id and lead.source_id not in partner.source_ids:
                    partner.source_ids += lead.source_id

    def set_referred(self):
        for partner in self:
            lead_partner_ids = self.env['crm.lead'].search([('partner_id', '=', partner.id)])
            partner.referred = ''
            for lead in lead_partner_ids:
                if partner.referred != '' and lead.referred:
                    partner.referred += ', {}'.format(lead.referred)
                elif partner.referred == '' and lead.referred:
                    partner.referred += '{}'.format(lead.referred)
