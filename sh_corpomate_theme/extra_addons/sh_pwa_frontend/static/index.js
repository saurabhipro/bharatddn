odoo.define("sh_corpomate_theme.pwa", function (require) {
    $(document).ready(function (require) {
        if ("serviceWorker" in navigator) {
            navigator.serviceWorker.register("/sh_corpomate_theme/firebase-messaging-sw.js").then(function () {
                console.log("Service Worker Registered");
            });
        }
    });
});
