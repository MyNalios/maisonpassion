# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MaisonPassionSaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_ref = fields.Char(related='partner_id.ref', string='Customer Code')
