from odoo import api, fields, models, _

from .base import DEFAULT_FIELDS


class SimplifiedDomain(models.Model):
    _name = 'simplified.domain'
    _description = 'Simplified Domain'
    _rec_name = 'model_id'

    model_id = fields.Many2one('ir.model', string='Model', required=True, ondelete='cascade')
    field_ids = fields.Many2many('ir.model.fields', string='Fields',)
    line_ids = fields.One2many('simplified.domain.line', 'simplified_domain_id', string='Additional Special Fields')

    _sql_constraints = [('unique_model_id', 'UNIQUE(model_id)', _('The Simplified Domain must by unique by model'))]


class SimplifiedDomainLine(models.Model):
    _name = 'simplified.domain.line'
    _description = 'Simplified Domain Line'

    simplified_domain_id = fields.Many2one(
        'simplified.domain', string='Simplified Domain', ondelete='cascade', index=True
    )
    model = fields.Char('Model Name', related='simplified_domain_id.model_id.model', store=True)
    technical_field = fields.Char('Technical Fields', required=True)
    label = fields.Char('Label', required=True, translate=True)

    final_field_name = fields.Char('Final Field Name', compute='_compute_final_field', store=True)
    final_field_model = fields.Char('Final Field Model', compute='_compute_final_field', store=True)
    comment = fields.Char('Comment', compute='_compute_comment')
    status = fields.Selection([('valid', 'Valid'), ('invalid', 'Invalid')], string='Status', compute='_compute_comment')

    @api.depends('technical_field', 'simplified_domain_id.field_ids')
    def _compute_comment(self):
        simplified_domain_obj = self.env['simplified.domain']
        ir_model_obj = self.env['ir.model']

        for line in self:
            errors = []
            chain = self.env[line.model].compute_chain(line.technical_field)

            while chain:
                field = chain.pop(0)

                model_id = ir_model_obj._get_id(field.model_name)
                model_simplified_domain = simplified_domain_obj.search([('model_id', '=', model_id)])
                if field.name in DEFAULT_FIELDS or not model_simplified_domain:
                    continue

                field_names = model_simplified_domain.field_ids.mapped('name')
                if field.name not in field_names:
                    model = self.env[field.model_name]
                    errors.append(
                        'The field %s must be added in the simplified domain of %s (%s)'
                        % (field.string, model._description, model._name)
                    )

            if errors:
                line.update({'status': 'invalid', 'comment': ' ----> '.join(errors)})
            else:
                line.status = 'valid'

    @api.depends('technical_field', 'simplified_domain_id.field_ids')
    def _compute_final_field(self):
        for line in self:
            chain = self.env[line.model].compute_chain(line.technical_field)

            if not chain:
                continue

            final_field = chain.pop()

            line.update({'final_field_name': final_field.name, 'final_field_model': final_field.model_name})
