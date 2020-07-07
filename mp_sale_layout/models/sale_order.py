# -*- coding: utf-8 -*-
from functools import partial
from odoo import api, fields, models
from odoo.tools.misc import formatLang


class MPSaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_distribution = fields.Selection([
        ('two_payments', '50-50'),
        ('three_payments', '40-50-10'),
        ], string='Payments Distribution', required=True, default='three_payments')
    first_payment = fields.Monetary(string='First Payment', store=True, compute='_compute_payments')
    second_payment = fields.Monetary(string='Second Payment', store=True, compute='_compute_payments')
    third_payment = fields.Monetary(string='Third Payment', store=True, compute='_compute_payments')
    available_delivery_address_ids = fields.Many2many('res.partner', 'sale_order_delivery_address_rel', 'sale_id',
                                                      'address_id', compute='_compute_available_delivery_address_ids',
                                                      help='Technical field used for delivery address domain')

    @api.depends('partner_id')
    def _compute_available_delivery_address_ids(self):
        for order in self:
            order.available_delivery_address_ids = self.env['res.partner']
            partner = order.partner_id
            if partner:
                shipping_addresses = partner.child_ids.filtered(lambda child: child.type == 'delivery')
                order.available_delivery_address_ids = shipping_addresses

    @api.depends('amount_total', 'payment_distribution')
    def _compute_payments(self):
        """Compute payments according to payment distribution (2 or 3 payments) """
        for order in self:
            if order.payment_distribution == 'two_payments':
                order.first_payment = order.second_payment = order.amount_total * 0.5
                order.third_payment = 0.0
            else:
                order.first_payment = order.amount_total * 0.4
                order.third_payment = order.amount_total * 0.1 if (order.amount_total * 0.1) <= 1000 else 1000
                order.second_payment = order.amount_total - order.first_payment - order.third_payment

    def _compute_amount_undiscounted(self):
        """Overwritten method
        Changes to discount computation (amount discount instead of % discount)"""
        for order in self:
            total = 0.0
            for line in order.order_line:
                # Changes here
                total += line.price_subtotal + (line.discount or 0.0) * line.product_uom_qty  # why is there a discount in a field named amount_undiscounted ??
            order.amount_undiscounted = total

    def _amount_by_group(self):
        """Overwritten method
        Changes to discount computation (amount discount instead of % discount)"""
        for order in self:
            currency = order.currency_id or order.company_id.currency_id
            fmt = partial(formatLang, self.with_context(lang=order.partner_id.lang).env, currency_obj=currency)
            res = {}
            for line in order.order_line:
                # Changes here
                price_reduce = line.price_unit - line.discount
                taxes = line.tax_id.compute_all(price_reduce, quantity=line.product_uom_qty, product=line.product_id, partner=order.partner_shipping_id)['taxes']
                for tax in line.tax_id:
                    group = tax.tax_group_id
                    res.setdefault(group, {'amount': 0.0, 'base': 0.0})
                    for t in taxes:
                        if t['id'] == tax.id or t['id'] in tax.children_tax_ids.ids:
                            res[group]['amount'] += t['amount']
                            res[group]['base'] += t['base']
            res = sorted(res.items(), key=lambda l: l[0].sequence)
            order.amount_by_group = [(
                l[0].name, l[1]['amount'], l[1]['base'],
                fmt(l[1]['amount']), fmt(l[1]['base']),
                len(res),
            ) for l in res]

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """
        Overwritten method
        Delivery address is no longer updated

        Update the following fields when the partner is changed:
        - Pricelist
        - Payment terms
        - Invoice address
        """
        if not self.partner_id:
            self.update({
                'partner_invoice_id': False,
                'partner_shipping_id': False,
                'fiscal_position_id': False,
            })
            return

        addr = self.partner_id.address_get(['delivery', 'invoice'])
        partner_user = self.partner_id.user_id or self.partner_id.commercial_partner_id.user_id
        values = {
            'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            'payment_term_id': self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.id or False,
            'partner_invoice_id': addr['invoice'],
            # Changes here
            # 'partner_shipping_id': addr['delivery'],
        }
        user_id = partner_user.id
        if not self.env.context.get('not_self_saleperson'):
            user_id = user_id or self.env.uid
        if self.user_id.id != user_id:
            values['user_id'] = user_id

        if self.env['ir.config_parameter'].sudo().get_param(
                'account.use_invoice_terms') and self.env.company.invoice_terms:
            values['note'] = self.with_context(lang=self.partner_id.lang).env.company.invoice_terms
        if not self.env.context.get('not_self_saleperson') or not self.team_id:
            values['team_id'] = self.env['crm.team']._get_default_team_id(
                domain=['|', ('company_id', '=', self.company_id.id), ('company_id', '=', False)], user_id=user_id)
        self.update(values)
