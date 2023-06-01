# -*- coding: utf-8 -*-

from odoo import models, api
from collections import OrderedDict


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def get_payment_term_lines_distribution(self):
        self.ensure_one()
        data = OrderedDict()
        amount_total = self.amount_total
        index_max = len(self.payment_term_id.line_ids) - 1
        for index, line in self.payment_term_id.line_ids.sorted(lambda x: x.sequence):
            amount = round(amount_total / 100 * line.value_amount, 2)
            if index == index_max:
                if line.max_amount and line.max_amount < amount:
                    to_report = amount - line.max_amount
                    amount = line.max_amount
                    data[index-1]['amount'] += to_report
            data[index] = {
                'text': line.distribution_text,
                'amount': amount
            }
        return data



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
