from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AdvancedDomainGenerator(models.TransientModel):
    _name = 'advanced.domain.generator'
    _description = 'Advanced Domain Generator'

    filter_domain = fields.Char()
    filter_domain_model = fields.Char('Filter Domain Model', required=True)
    target_id = fields.Integer('Target ID', required=1)
    target_model = fields.Char('Target Model', required=1)
    target_field_name = fields.Char('Target Field Name', required=1)
    is_simplified_domain = fields.Boolean('Simplified domain')

    @api.model
    def open_wizard(self, record, filter_domain_model, target_field_name='filter_domain', is_simplified_domain=False):
        record.ensure_one()

        if filter_domain_model not in self.env:
            raise ValidationError(_('Invalid model for domain'))

        if target_field_name not in record._fields:
            raise ValidationError(_('The field %s is not a field of %s') % (target_field_name, record._name))
        filter_domain = getattr(record, target_field_name)

        wizard = self.create(
            {
                'filter_domain_model': filter_domain_model,
                'target_id': record.id,
                'target_model': record._name,
                'target_field_name': target_field_name,
                'filter_domain': filter_domain,
                'is_simplified_domain': is_simplified_domain,
            }
        )

        action = self.env.ref('advanced_domain_generator.action_advanced_domain_generator').read()[0]
        action.update({'res_id': wizard.id})

        return action

    def validate_domain(self):
        self.ensure_one()

        self.env[self.target_model].browse(self.target_id).write({self.target_field_name: self.filter_domain})
