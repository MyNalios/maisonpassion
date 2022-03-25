# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Partner(models.Model):
    _inherit = 'res.partner'

    document_ids = fields.Many2many('sale.technical.document', 'technical_document_partner_rel', 'partner_id', 'document_id', string='Technical Documents')
    documents_count = fields.Integer('# Technical Documents', help='Number of technical documents accessible by current partner on portal',
                                  compute='_compute_documents_count', compute_sudo=True)

    @api.depends('document_ids')
    def _compute_documents_count(self):
        for partner in self:
            partner.documents_count = len(partner.document_ids)

    def show_documents_action(self):
        """ display tree view of technical documents related to current partner """
        self.ensure_one()
        return {
            'name': _('Documents'),
            'view_mode': 'tree,form',
            'res_model': 'sale.technical.document',
            'type': 'ir.actions.act_window',
            'context': {'create': False, 'delete': False},
            'domain': [('partner_ids', '=', self.id)],
            'target': 'current',
        }
