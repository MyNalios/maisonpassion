# -*- coding: utf-8 -*-

from odoo import fields, models


class MaisonPassionResPartner(models.Model):
    _inherit = 'res.partner'

    referred_partner_id = fields.Many2one('res.partner', string='Referred By', domain=[('type', '=', 'contact')])
