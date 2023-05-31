# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    
    
    def _convert_to_tax_base_line_dict(self):
        data = super()._convert_to_tax_base_line_dict()
        if self.discount_eur:
            data.update({'price_subtotal': data.get('price_subtotal') - self.discount_eur})
        data['discount_eur'] = self.discount_eur
        return data
    
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id','discount_eur')
    def _compute_amount(self):
        super()._compute_amount()

