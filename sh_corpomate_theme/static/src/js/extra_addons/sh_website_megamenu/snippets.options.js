/** @odoo-module **/


import options from "@web_editor/js/editor/snippets.options";

options.registry.MegaMenuLayout.include({


    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @private
     * @returns {string} xmlid of the current template.
     */
    _getCurrentTemplateXMLID: function () {

        var has_section = this.containerEl.querySelector('section') || false
        if (has_section){
            
            var templateDefiningClass = has_section.classList.value.split(' ').filter(cl => cl.startsWith('sh_website_megamenu'))[0];

            templateDefiningClass = templateDefiningClass || false;
            if(templateDefiningClass){
                var modifiedTemplateDefiningClass = templateDefiningClass.replace('sh_website_megamenu_', '');
                return `sh_corpomate_theme.${modifiedTemplateDefiningClass}`;
            }

        }

        return this._super(...arguments);

    },



});
