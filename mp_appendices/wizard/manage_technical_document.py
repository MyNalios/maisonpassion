# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class ManageDocumentWizard(models.TransientModel):
    _name = 'manage.technical.document'
    _description = 'Manage technical documents accessible by partner'

    def _default_partner_ids(self):
        """ Retrieve active partner from context """
        partner_ids = self._context.get('active_model') == 'res.partner' and self._context.get('active_ids') or False
        return [
            (4, partner.id, 0)
            for partner in self.env['res.partner'].browse(partner_ids)
        ]

    def _default_document_ids(self):
        """ Retrieve documents related to active partner in context """
        partner_ids = self._context.get('active_model') == 'res.partner' and self._context.get('active_ids') or False
        if partner_ids:
            return [(4, doc.id, 0) for doc in self.env['res.partner'].browse(partner_ids).document_ids]
        return partner_ids

    partner_ids = fields.Many2many('res.partner', 'document_partner_wizard_rel', 'wizard_id', 'partner_id', string='Partners', required=True, default=_default_partner_ids)
    document_ids = fields.Many2many('sale.technical.document', 'partner_document_wizard_rel', 'wizard_id', 'document_id', string="Technical Documents", default=_default_document_ids)

    def button_save(self):
        """ Save each document in each partner """
        self.ensure_one()
        if self.partner_ids:
            for partner in self.partner_ids:
                partner.write({'document_ids': [(6, 0, self.document_ids.ids)]})
        else:
            raise ValidationError(_('Partner field should be set before applying changes'))
        return {'type': 'ir.actions.act_window_close'}
