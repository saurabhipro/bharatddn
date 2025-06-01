/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.WebsitePreloader = publicWidget.Widget.extend({
    selector: ".js_cls_custom_website_preloader",
    start: function () {
        var self = this
        var $preloader = self.$el
        $preloader.css({ display: "block" });
        $("body").css({ overflow: "visible" });
        $preloader.delay(1500).fadeOut("slow");
        $("body").delay(1500).css({ overflow: "visible" });
        this._super.apply(this, arguments);
    },
});

