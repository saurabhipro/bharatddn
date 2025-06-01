/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";


publicWidget.registry.pwa = publicWidget.Widget.extend({
    selector: '#wrapwrap',
    start: function () {

        // PWA for corpomate frontend
        this._super.apply(this, arguments);
        if (this.$target.data("sh_pwa_frontend") == "True") {
            navigator.serviceWorker.register("/sh_corpomate_theme/firebase-messaging-sw.js").then(function () {
                console.log("Service Worker Registered");
            });

        }
    },
});

