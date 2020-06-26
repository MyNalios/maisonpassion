# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MPSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    discount = fields.Float(string='Discount (EUR)', digits='Product Price', default=0.0)

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """Overwritten method
        Changes to discount computation (amount discount instead of % discount)"""
        for line in self:
            # changes here
            price = line.price_unit - (line.discount or 0.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])

    @api.depends('price_unit', 'discount')
    def _get_price_reduce(self):
        """Overwritten method
        Changes to discount computation (amount discount instead of % discount)"""
        for line in self:
            # changes here
            line.price_reduce = line.price_unit - line.discount
