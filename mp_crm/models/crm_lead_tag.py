# -*- coding: utf-8 -*-
from odoo import fields, models


class Tag(models.Model):
    _inherit = 'crm.lead.tag'
    _sql_constraints = [
        ('tech_name_uniq', 'unique (technical_name)', 'Technical name must be unique !'),
    ]

    technical_name = fields.Char(string='Technical Name')
