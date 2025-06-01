/** @odoo-module **/

import { LinkDialog } from "./widgets/link_dialog";

LinkDialog.include({

	xmlDependencies: (weWidgets.LinkDialog.prototype.xmlDependencies || []).concat(
        ['/sh_corpomate_theme/static/src/xml/website.editor.xml']
    ),

    
    /**
     * @constructor
     */
    init: function () {
        this._super.apply(this, arguments);
                
        var allBtnClassSuffixes = /(^|\s+)btn(-[a-z0-9_-]*)?/gi;
        //var allBtnShapes = /\s*(rounded-circle|flat)\s*/gi;
        var allBtnShapes = /\s*(rounded-circle|flat|sh_btn_cm_1|sh_btn_cm_2|sh_btn_cm_3|sh_btn_cm_4|sh_btn_cm_5|sh_btn_cm_6|sh_btn_cm_7|sh_btn_cm_8)\s*/gi;        
        this.data.className = this.data.iniClassName
            .replace(allBtnClassSuffixes, ' ')
            .replace(allBtnShapes, ' ');        
        
    },    
    
    
});
