# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Lead2OpportunityPartner(models.TransientModel):

    _inherit = 'crm.lead2opportunity.partner'

    source_id = fields.Many2one('utm.source', 'Source', required=True, help="This is the source of the lead, e.g. Search Engine, Website, Social Media")

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
        return super(Lead2OpportunityPartner, self).action_apply()