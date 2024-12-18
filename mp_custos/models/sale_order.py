# -*- coding: utf-8 -*-

from odoo import models, api, fields
from collections import OrderedDict


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    user_id = fields.Many2one('res.users', string='Project Responsible')
    validity_date = fields.Date(required=True)

    def get_payment_term_lines_distribution(self):
        self.ensure_one()
        data = OrderedDict()
        amount_total = self.amount_total
        index_max = len(self.payment_term_id.line_ids) - 1
        for index, line in enumerate(self.payment_term_id.line_ids.sorted(lambda x: x.sequence)):
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
        calculated_amount = sum(d['amount'] for d in data.values())
        if calculated_amount != amount_total:
            missing_cents = amount_total - calculated_amount
            data[index_max-1]['amount'] += missing_cents
        return data



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _convert_to_tax_base_line_dict(self, **kwargs):
        data = super()._convert_to_tax_base_line_dict(**kwargs)
        if self.discount_eur:
            if data['quantity'] == 1:
                data['price_unit'] -= self.discount_eur
                data['price_subtotal'] -= self.discount_eur
            elif data['quantity'] > 1:
                qty = data['quantity']
                data['quantity'] = 1
                data['price_unit'] = data['price_unit'] * qty - self.discount_eur
                data['price_subtotal'] = data['price_subtotal'] * qty - self.discount_eur
        return data
    
    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        if self.discount_eur and not self.discount:
            discount = self.discount_eur / self.price_unit * 100
            res['discount'] = discount
            res['discount_eur'] = self.discount_eur
        return res
