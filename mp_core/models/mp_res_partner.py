# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MaisonPassionResPartner(models.Model):
    _inherit = 'res.partner'

    mobile = fields.Char(string='Mobile 1')
    mobile_2 = fields.Char(string='Mobile 2')
    email_2 = fields.Char(string='Email 2')
    is_client_effective = fields.Boolean(string='Effective Client', compute='_compute_is_client_effective',
                                         readonly=True)
    source_ids = fields.Many2many('utm.source', 'partner_crm_source_rel', 'partner_id', 'source_id', string='Sources'
                                  , compute='_compute_source_ids', store=True, readonly=False)
    referred = fields.Char(string='Referred By', compute='_compute_referred', readonly=False)

    # @api.constrains('ref')
    # def _check_unique_ref(self):
    #     for partner in self:
    #         if not partner.parent_id and partner.ref:
    #             result = self.search([('id', '!=', partner.id), ('id', 'not in', partner.child_ids.ids),
    #                                   ('ref', '=', partner.ref)], limit=1)
    #             if result:
    #                 message = _("You have already a partner ({}) with this reference ({})".format(result.name,
    #                                                                                               partner.ref))
    #                 raise ValidationError(message)

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

        # CHanger la méthode. Soit en cachant le champ référence du parent_id, soit via compute & store avec depends sur parent_id
        # partner_need_ref = self.env['res.partner']
        # for partner in self:
        #     if partner.parent_id and not vals.get('parent_id', True) and not vals.get('ref', False):
        #         partner_need_ref |= partner
        #         sequence = self.env['ir.sequence'].next_by_code("res.partner")
        #         print(partner, sequence)
        #         vals.update({'ref': sequence})
        #         partner.write(vals)
        # return super(MaisonPassionResPartner, self-partner_need_ref).write(vals)

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
        return ['vat', 'credit_limit', 'ref']

    @api.depends('sale_order_ids')
    def _compute_is_client_effective(self):
        for partner in self:
            if partner.sale_order_ids:
                partner.is_client_effective = True
            else:
                partner.is_client_effective = False

    @api.depends('opportunity_ids.source_id')
    def _compute_source_ids(self):
        for partner in self:
            if partner.opportunity_ids:
                for lead in partner.opportunity_ids:
                    if lead.source_id and lead.source_id not in partner.source_ids:
                        partner.source_ids += lead.source_id

    @api.depends('opportunity_ids.referred')
    def _compute_referred(self):
        for partner in self:
            if partner.opportunity_ids:
                for lead in partner.opportunity_ids:
                    partner.referred = ''
                    if partner.referred != '' and lead.referred:
                        partner.referred += ', {}'.format(lead.referred)
                    elif partner.referred == '' and lead.referred:
                        partner.referred += '{}'.format(lead.referred)
            else:
                partner.referred = ''
