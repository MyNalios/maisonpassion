odoo.define("advanced_domain_generator.ModelFieldSelector", function (require) {
    "use strict";

    const core = require("web.core");
    const ModelFieldSelector = require("web.ModelFieldSelector");

    var modelFieldsCache = {
        cache: {},
        cacheDefs: {},
    };

    core.bus.on('clear_cache', null, function () {
        modelFieldsCache.cache = {};
        modelFieldsCache.cacheDefs = {};
    });

    ModelFieldSelector.include({
        _getModelFieldsFromCache: function (model, filters) {
            const self = this;

            const context = _.extend({
                is_simplified_domain: self.options.is_simplified_domain
            }, self.getSession().user_context);

            const cache_key = model + self.options.is_simplified_domain;

            let def = modelFieldsCache.cacheDefs[cache_key];
            if (!def) {
                def = modelFieldsCache.cacheDefs[cache_key] = this._rpc({
                        model: model,
                        method: 'fields_get',
                        args: [
                            false,
                            ["store", "searchable", "type", "string", "relation", "selection", "related"]
                        ],
                        context: context,
                    })
                    .then((function (fields) {
                        modelFieldsCache.cache[cache_key] = sortFields(fields, model, self.options.order);
                    }).bind(this));
            }
            return def.then((function () {
                const result = _.filter(modelFieldsCache.cache[cache_key], function (f) {
                    return (!filters.searchable || f.searchable) && self.options.filter(f);
                });
                return result
            }).bind(this));
        },
    });

    function sortFields(fields, model, order) {
        var array = _.chain(fields)
            .pairs()
            .sortBy(function (p) { return p[1].string; });
        if (order !== 'string') {
            array = array.sortBy(function (p) {return p[1][order]; });
        }
        return array.map(function (p) {
                return _.extend({
                    name: p[0],
                    model: model,
                }, p[1]);
            }).value();
    }
});
