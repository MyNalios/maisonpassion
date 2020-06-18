import functools
import logging

from odoo import api, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

DEFAULT_FIELDS = {'id', 'name'}


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        if not self.env.context.get('is_simplified_domain'):
            return super().fields_get(allfields=allfields, attributes=attributes)

        result = super().fields_get(allfields=allfields, attributes=attributes)

        model_id = self.env['ir.model']._get_id(self._name)

        query = """
        SELECT imf.name
        FROM ir_model_fields_simplified_domain_rel rel
            INNER JOIN ir_model_fields imf on rel.ir_model_fields_id = imf.id
            INNER JOIN simplified_domain sd on rel.simplified_domain_id = sd.id
        WHERE sd.model_id = %s
        """

        self.env.cr.execute(query, (model_id,))
        field_names = [x[0] for x in self.env.cr.fetchall()]

        if field_names:
            result = {key: value for key, value in result.items() if key in set(field_names) | DEFAULT_FIELDS}

        special_fields = {}
        lines = self.env['simplified.domain.line'].search([('model', '=', self._name)])
        for line in lines:
            model = self.env[line.final_field_model]
            field = model._fields[line.final_field_name]

            has_access = functools.partial(model.check_access_rights, raise_exception=False)
            readonly = not (has_access('write') or has_access('create'))

            if field.groups and not self.user_has_groups(field.groups):
                continue

            description = field.get_description(self.env)
            description['string'] = line.label

            if readonly:
                description['readonly'] = True
                description['states'] = {}
            if attributes:
                description = {key: val for key, val in description.items() if key in attributes}
            special_fields[line.technical_field] = description

        result.update(special_fields)

        return result

    @api.model
    def compute_chain(self, technical_field):
        chain = []
        if not technical_field:
            return chain

        field_list = technical_field.split('.')

        current_model = None
        current_field_name = None
        while field_list:
            current_field_name = field_list.pop(0)
            if current_model is None:
                current_model = self.env[self._name]

            if current_field_name not in current_model._fields:
                raise ValidationError(
                    _('Invalid technical name. The field %s doesn\'t exist in the model %s')
                    % (current_field_name, current_model._name)
                )
            current_field = current_model._fields[current_field_name]

            if not current_field.relational and field_list:
                raise ValidationError(
                    _('Invalid technical name. The field %s on the model %s is not relational.')
                    % (current_field_name, current_model._name)
                )
            elif current_field.relational and field_list:
                current_model = self.env[current_field.comodel_name]

            chain.append(current_field)

        if current_model is None or current_field_name is None:
            raise ValidationError(_('Invalid technical name.'))

        return chain
