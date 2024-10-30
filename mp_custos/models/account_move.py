# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    is_hide_discount = fields.Boolean(string='Hide Discount', default=False, compute='_compute_hide_discount')

    def _compute_hide_discount(self):
        for move in self:
            move.is_hide_discount = all(not line.discount_eur for line in move.line_ids)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    discount_eur = fields.Float(string='Discount (EUR)', digits='Product Price', default=0.0, compute='_compute_discount', store=True, readonly=False)
    discount = fields.Float( string='Discount (%)', digits='Discount', default=0.0, compute='_compute_discount', store=True, readonly=False)
    is_hide_discount = fields.Boolean(string='Hide Discount', default=False, related='move_id.is_hide_discount')

    @api.depends('discount_eur', 'discount','price_unit')
    def _compute_discount(self):
        for line in self:

            if line._origin.discount_eur != line.discount_eur:
                line.discount = line.discount_eur / line.price_unit * 100
            # elif line._origin.discount != line.discount:
            #     line.discount_eur = 0.0

