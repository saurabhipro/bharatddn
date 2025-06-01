/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.WebsiteSProgress = publicWidget.Widget.extend({
    selector: ".js_cls_render_dynamic_progress_area",
    start: function () {
        var self = this
        var $progress_el_holders = self.$el
        if ($progress_el_holders && $progress_el_holders.length) {
            // DOM ELEMENTS
            $progress_el_holders.each(function () {
                var percent = $(this).find(".js_cls_s_progress_percent_manual_span").text() || "0%";


                $(this).find(".js_cls_s_progress_percent_auto_style").css("width", percent);
            });
        }


        this._super.apply(this, arguments);
    }
});
