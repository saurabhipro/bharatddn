/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";


publicWidget.registry.ShWebsiteEditorCorpomate = publicWidget.Widget.extend({
    selector: "#wrapwrap",
    disabledInEditableMode: true,

    /**
     * @constructor
     */
    init: function () {
        this._super.apply(this, arguments);
        
    },    


    destroy: function () {
        var self = this;
        
        this._super.apply(this, arguments);
        $('section.o_footer_copyright').find('a').addClass('oe_edited_link')
        $('section.o_footer_copyright').find('a').attr('contenteditable','true')
    },    

    
});
