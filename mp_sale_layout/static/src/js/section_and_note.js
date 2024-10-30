odoo.define('mp_sale_layout.section_and_note_custom', function(require){

    "use strict";
    var section_and_note = require('account.section_and_note_backend');

    section_and_note.include({
        _renderBodyCell: function (record, node, index, options) {
            var $cell = this._super.apply(this, arguments);
    
            var isSection = record.data.display_type === 'line_section';
            var isNote = record.data.display_type === 'line_note';
            var isBreak = record.data.display_type === 'line_break';
            if (isSection || isNote || isBreak) {
                if (node.attrs.widget === "handle") {
                    return $cell;
                } else if (node.attrs.name === "name") {
                    var nbrColumns = this._getNumberOfCols();
                    if (this.handleField) {
                        nbrColumns--;
                    }
                    if (this.addTrashIcon) {
                        nbrColumns--;
                    }
                    $cell.attr('colspan', nbrColumns);
                } else {
                    $cell.removeClass('o_invisible_modifier');
                    return $cell.addClass('o_hidden');
                }
            }
            
            return $cell;
        },
    })

    return section_and_note
    
})