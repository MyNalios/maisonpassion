# -*- coding: utf-8 -*-
from odoo import fields, models


class UtmSource(models.Model):
    _inherit = 'utm.source'
    _sql_constraints = [
        ('tech_name_uniq', 'unique (technical_name)', 'Technical name must be unique !'),
    ]

    technical_name = fields.Char(string='Technical Name')