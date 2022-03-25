# -*- coding: utf-8 -*-
from odoo import fields, models


class LeadCreationLog(models.Model):
    _name = 'crm.lead.creation.log'
    _description = 'Log of Lead Creation Requests from External Source'

    url = fields.Char(string='URL')
    method = fields.Char(string='Method')
    charset = fields.Char(string='Charset')
    content_type = fields.Char(string='Content Type')
    mimetype = fields.Char(string='Mime Type')
    params = fields.Text(string='Params')
    form_data = fields.Text(string='Form Data')

