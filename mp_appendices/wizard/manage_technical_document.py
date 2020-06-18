# -*- coding: utf-8 -*-

from odoo import fields, models, _


class ManageDocumentWizard(models.TransientModel):
    _name = 'manage.technical.document'
    _description = 'Manage technical documents accessible by user'

    def _default_user_id(self):
        user_id = self._context.get('active_model') == 'res.users' and self._context.get('active_id') or False
        return self.env['res.users'].browse(user_id)

    def _default_document_ids(self):
        user_id = self._context.get('active_model') == 'res.users' and self._context.get('active_id') or False
        if user_id:
            return [(4, doc.id, 0) for doc in self.env['res.users'].browse(user_id).document_ids]
        return user_id

    user_id = fields.Many2one('res.users', string='User', default=_default_user_id)
    document_ids = fields.Many2many('sale.technical.document', 'user_document_wizard_rel', 'wizard_id', 'document_id', string="Technical Documents", default=_default_document_ids)

    def button_save(self):
        self.ensure_one()
        if self.user_id:
            self.user_id.write({'document_ids': [(6, 0, self.document_ids.ids)]})
        else:
            return {'warning': _('User field should be set before applying changes')}
        return {'type': 'ir.actions.act_window_close'}
