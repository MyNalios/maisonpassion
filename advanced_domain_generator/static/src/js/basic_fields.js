odoo.define("advanced_domain_generator.basic_fields", function (require) {

"use strict";

const basic_fields = require('web.basic_fields');
const session = require('web.session');

const AdvancedDomainSelector = require('advanced_domain_generator.AdvancedDomainSelector');

basic_fields.FieldDomain.include({
    _render: function () {
        // If there is no model, only change the non-domain-selector content
        if (!this._domainModel) {
            this._replaceContent();
            return $.when();
        }

        // Convert char value to array value
        var value = this.value || "[]";

        // Create the domain selector or change the value of the current one...
        var def;
        if (!this.domainSelector) {
            this.domainSelector = new AdvancedDomainSelector(this, this._domainModel, value, {
                readonly: this.mode === "readonly" || this.inDialog,
                filters: this.fsFilters,
                debugMode: session.debug,
                is_simplified_domain: this.recordData.is_simplified_domain,
                default: [["id", "=", 0]]
            });
            def = this.domainSelector.prependTo(this.$el);
        } else {
            def = this.domainSelector.setDomain(value);
        }
        // ... then replace the other content (matched records, etc)
        return def.then(this._replaceContent.bind(this));
    },
});

});
