# -*- coding: utf-8 -*-

from odoo import models


class AccountTax(models.Model):
    _inherit = 'account.tax'

    def _compute_taxes_for_single_line(self, base_line, handle_price_include=True, include_caba_tags=False, early_pay_discount_computation=None, early_pay_discount_percentage=None):
        vals = super()._compute_taxes_for_single_line(base_line, handle_price_include=True, include_caba_tags=False, early_pay_discount_computation=None, early_pay_discount_percentage=None)
        
        if 'discount_eur' in base_line and base_line['discount_eur']:
            vals[0].update({'price_subtotal': vals[0].get('price_subtotal') - base_line['discount_eur']})
        return vals