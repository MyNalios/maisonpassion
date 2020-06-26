# -*- coding: utf-8 -*-

from odoo import fields, models

class MaisonPassionSaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_ref = fields.Char(related='partner_id.ref', string='Customer Code')
