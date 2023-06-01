# -*- coding: utf-8 -*-

from odoo import models, fields


class PaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    is_personalized = fields.Boolean('Is a personalized distribution')

class PaymentTermLine(models.Model):
    _inherit = 'account.payment.term.line'

    sequence = fields.Integer(string="Sequence")
    max_amount = fields.Float(string="Maximum amount")
    distribution_text = fields.Char(string="Distribution text")
