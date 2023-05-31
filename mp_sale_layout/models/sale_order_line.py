# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MPSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    discount_eur = fields.Float(string='Discount (EUR)', digits='Product Price', default=0.0)
    validation_date = fields.Date(string="Validation date")
    display_type = fields.Selection(selection_add=[('line_break', 'Page break')])
    # price_subtotal = fields.Monetary(compute='_compute_amount', inverse='_inverse_price_subtotal', string='Subtotal',
    #                                  readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, store=True)

    # def _inverse_price_subtotal(self):
    #     for line in self:
    #         price_unit = line.price_subtotal * 1.3 if line.price_subtotal * 1.3 < line.price_subtotal + 5000 \
    #             else line.price_subtotal + 5000
    #         discount = line.price_subtotal - price_unit
    #         taxes = line.tax_id.compute_all(line.price_subtotal, line.order_id.currency_id, line.product_uom_qty,
    #                                         product=line.product_id, partner=line.order_id.partner_shipping_id)
    #         line.update({
    #             'price_unit': price_unit,
    #             'discount': discount,
    #             'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
    #             'price_total': taxes['total_included'],
    #         })

    # @api.depends('price_unit', 'discount_eur')
    # def _get_price_reduce(self):
    #     #TODO 
    #     """Overwritten method
    #     Changes to discount computation (amount discount instead of % discount)"""
    #     for line in self:
    #         # changes here
    #         line.price_reduce = line.price_unit - line.discount_eur

