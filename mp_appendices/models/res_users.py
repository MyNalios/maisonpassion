# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Users(models.Model):
    _inherit = 'res.users'

    document_ids = fields.Many2many('sale.technical.document', 'technical_document_user_rel', 'user_id', 'document_id', string='Technical Documents')
    documents_count = fields.Integer('# Technical Documents', help='Number of technical documents accessible by current user on portal',
                                  compute='_compute_documents_count', compute_sudo=True)

    @api.depends('document_ids')
    def _compute_documents_count(self):
        for user in self:
            user.documents_count = len(user.document_ids)

    def show_documents_action(self):
        self.ensure_one()
        return {
            'name': _('Documents'),
            'view_mode': 'tree,form',
            'res_model': 'sale.technical.document',
            'type': 'ir.actions.act_window',
            'context': {'create': False, 'delete': False},
            'domain': [('user_ids', '=', self.id)],
            'target': 'current',
        }
