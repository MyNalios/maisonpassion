# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleTechnicalDocument(models.Model):
    _name = 'sale.technical.document'
    _inherit = ['portal.mixin']
    _description = 'Technical Documents for Customers'

    name = fields.Char(string='Document Name', required=True)
    user_ids = fields.Many2many('res.users', 'technical_document_user_rel', 'document_id', 'user_id', string='Users')
    attachment_id = fields.Many2one('ir.attachment', string='Attachment', domain="[('res_model', '=', 'sale.technical.document')]", attachment=True)
    tag_ids = fields.Many2many('sale.technical.document.tag', 'technical_document_tag_rel', 'technical_document_id', 'tag_id', string='Tags')
