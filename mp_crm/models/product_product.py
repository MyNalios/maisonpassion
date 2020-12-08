# -*- coding: utf-8 -*-

from odoo import models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def get_product_multiline_description_sale(self):
        """ Overwritten method
            Remove display name from sale description
        """
        name = ''
        if self.description_sale:
            name = self.description_sale
        return name
