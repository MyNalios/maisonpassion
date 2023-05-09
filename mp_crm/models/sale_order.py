# -*- coding: utf-8 -*-
from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # @api.onchange('partner_id')
    # def onchange_partner_id(self):
    #     super(SaleOrder, self).onchange_partner_id()
    #     if self.env.context.get('default_user_id'):
    #         self.update({'user_id': self.env.context.get('default_user_id')})
