# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    is_personalized = fields.Boolean('Is a personalized distribution')

    @api.constrains('line_ids')
    def _check_lines(self):
        for terms in self:
            if not terms.is_personalized and  len(terms.line_ids.filtered(lambda r: r.value == 'balance')) != 1:
                raise ValidationError(_('The Payment Term must have one Balance line.'))
            if terms.line_ids.filtered(lambda r: r.value == 'fixed' and r.discount_percentage):
                raise ValidationError(_("You can't mix fixed amount with early payment percentage"))


class PaymentTermLine(models.Model):
    _inherit = 'account.payment.term.line'

    sequence = fields.Integer(string="Sequence")
    max_amount = fields.Float(string="Maximum amount")
    distribution_text = fields.Char(string="Distribution text")
