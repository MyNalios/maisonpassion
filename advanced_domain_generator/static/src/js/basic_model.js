odoo.define("advanced_domain_generator.basic_model", function (require) {

"use strict";

const BasicModel = require('web.BasicModel');


BasicModel.include({
    _fetchSpecialDomain: function (record, fieldName, fieldInfo) {
        if (!fieldInfo.options.use_field_as_model || !record.data || !record.data[fieldInfo.options.use_field_as_model]) {
            return this._super.apply(this, arguments);
        }

        fieldInfo.options.model = record.data[fieldInfo.options.use_field_as_model];
        return this._super.apply(this, arguments);
    },
});

});
