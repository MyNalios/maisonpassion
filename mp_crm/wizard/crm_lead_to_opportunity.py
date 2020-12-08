# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Lead2OpportunityPartner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    source_id = fields.Many2one('utm.source', 'Source', help='This is the source of the lead, e.g. Search Engine, Website, Social Media')
    partner_source_id = fields.Many2one('utm.source', 'Source', help='This is the source of the customer, e.g. Search Engine, Website, Social Media')

    @api.onchange('partner_id')
    def _onchange_existing_partner_id(self):
        if self.partner_id:
            self.update({'partner_source_id': self.partner_id.source_id.id})

    @api.model
    def default_get(self, fields):
        """ Overridden method
        """
        result = super(Lead2OpportunityPartner, self).default_get(fields)
        if self._context.get('active_id'):

            lead = self.env['crm.lead'].browse(self._context['active_id'])
            if 'source_id' in fields and lead.source_id:
                result['source_id'] = lead.source_id.id

        return result

    def action_apply(self):
        """ Overridden method
        """
        self.ensure_one()
        if self.source_id and self.action == 'create':
            leads = self.env['crm.lead'].browse(self._context.get('active_ids', []))
            leads.update({'source_id': self.source_id.id})
        if self.partner_source_id and self.partner_id and self.action == 'exist':
            self.partner_id.update({'source_id': self.partner_source_id.id})
            leads = self.env['crm.lead'].browse(self._context.get('active_ids', []))
            leads.update({'source_id': self.partner_source_id.id})
        return super(Lead2OpportunityPartner, self).action_apply()