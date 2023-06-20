# -*- coding: utf-8 -*-
# from functools import partial
from odoo import api, fields, models
# from odoo.tools.misc import formatLang


class MPSaleOrder(models.Model):
    _inherit = 'sale.order'

    # payment_distribution = fields.Selection([
    #     ('two_payments', '50-50'),
    #     ('three_payments', '40-50-10'),
    #     ], string='Payments Distribution', required=True, default='three_payments')
    # first_payment = fields.Monetary(string='First Payment', store=True, compute='_compute_payments')
    # second_payment = fields.Monetary(string='Second Payment', store=True, compute='_compute_payments')
    # third_payment = fields.Monetary(string='Third Payment', store=True, compute='_compute_payments')
    # A checker
    # available_delivery_address_ids = fields.Many2many('res.partner', 'sale_order_delivery_address_rel', 'sale_id',
    #                                                   'address_id', compute='_compute_available_delivery_address_ids',
    #                                                   help='Technical field used for delivery address domain')
    # information_message = fields.Text('Information Message')
    # change label
    
    # change required

    
    # A checker
    # @api.depends('partner_id')
    # def _compute_available_delivery_address_ids(self):
    #     for order in self:
    #         order.available_delivery_address_ids = self.env['res.partner']
    #         partner = order.partner_id
    #         if partner:
    #             shipping_addresses = partner.child_ids.filtered(lambda child: child.type == 'delivery')
    #             order.available_delivery_address_ids = shipping_addresses + partner

    # @api.depends('amount_total', 'payment_distribution')
    # def _compute_payments(self):
    #     """Compute payments according to payment distribution (2 or 3 payments) """
    #     for order in self:
    #         if order.payment_distribution == 'two_payments':
    #             order.first_payment = order.second_payment = order.amount_total * 0.5
    #             order.third_payment = 0.0
    #         else:
    #             order.first_payment = order.amount_total * 0.4
    #             order.third_payment = order.amount_total * 0.1 if (order.amount_total * 0.1) <= 1000 else 1000
    #             order.second_payment = order.amount_total - order.first_payment - order.third_payment


    # a checker
    # def _compute_amount_undiscounted(self):
    #     """
    #     Overwritten method
    #     Changes to discount computation (amount discount instead of % discount)
    #     """
    #     for order in self:
    #         total = 0.0
    #         for line in order.order_line:
    #             # Changes here to discount computation (amount instead of %)
    #             total += line.price_subtotal + (line.discount_eur or 0.0) * line.product_uom_qty  # why is there a discount in a field named amount_undiscounted ??
    #         order.amount_undiscounted = total

    # a checker
    # def _amount_by_group(self):
    #     """
    #     Overwritten method
    #     Changes to discount computation (amount discount instead of % discount)
    #     """
    #     for order in self:
    #         currency = order.currency_id or order.company_id.currency_id
    #         fmt = partial(formatLang, self.with_context(lang=order.partner_id.lang).env, currency_obj=currency)
    #         res = {}
    #         for line in order.order_line:
    #             # Changes here to discount computation (amount instead of %)
    #             price_reduce = line.price_unit - line.discount_eur
    #             taxes = line.tax_id.compute_all(price_reduce, quantity=line.product_uom_qty, product=line.product_id, partner=order.partner_shipping_id)['taxes']
    #             for tax in line.tax_id:
    #                 group = tax.tax_group_id
    #                 res.setdefault(group, {'amount': 0.0, 'base': 0.0})
    #                 for t in taxes:
    #                     if t['id'] == tax.id or t['id'] in tax.children_tax_ids.ids:
    #                         res[group]['amount'] += t['amount']
    #                         res[group]['base'] += t['base']
    #         res = sorted(res.items(), key=lambda l: l[0].sequence)
    #         order.amount_by_group = [(
    #             l[0].name, l[1]['amount'], l[1]['base'],
    #             fmt(l[1]['amount']), fmt(l[1]['base']),
    #             len(res),
    #         ) for l in res]

    # @api.onchange('partner_id')
    # def onchange_partner_id(self):
    #     """
    #     Overridden method
    #     Delivery address is no longer updated according to partner_id
    #     """
    #     super(MPSaleOrder, self).onchange_partner_id()
    #     self.update({'partner_shipping_id': False,})

