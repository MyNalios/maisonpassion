# -*- coding: utf-8 -*-
from odoo import fields, models, _


class TechnicalDocumentTag(models.Model):
    _name = 'sale.technical.document.tag'
    _description = 'Technical Document Tag'
    _sql_constraints = [
        ('tag_name_unique', 'unique (name)', _('Tag name already exists.')),
    ]

    name = fields.Char(string='Tag Name', required=True, translate=True)
    color = fields.Integer(string='Color Index')
