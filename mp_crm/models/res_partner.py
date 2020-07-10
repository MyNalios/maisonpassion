# -*- coding: utf-8 -*-

from odoo import api, fields, models


class MaisonPassionResPartner(models.Model):
    _inherit = 'res.partner'

    referred_partner_ids = fields.Many2many('res.partner', 'partner_referred_rel', 'partner_id', 'partner_referred_id', compute='_compute_referred_partner_ids', readonly=False, store=True, string='Referred By')

    @api.depends('opportunity_ids.referred_partner_ids')
    def _compute_referred_partner_ids(self):
        for partner in self:
            if partner.opportunity_ids:
                for lead in partner.opportunity_ids:
                    partner.update({
                        'referred_partner_ids': [(4, partner.id) for partner in lead.referred_partner_ids]
                    })
