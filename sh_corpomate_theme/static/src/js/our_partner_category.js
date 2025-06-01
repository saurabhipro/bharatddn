/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { KeepLast } from "@web/core/utils/concurrency";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.ShOurPartnerWithCategorySelection = publicWidget.Widget.extend({
    selector: ".js_cls_our_partners_with_category_selection",
    disabledInEditableMode: true,

    /**
     * @constructor
     */
    init: function () {
        this._super.apply(this, arguments);
        this.KeepLast = new KeepLast()
    },

    /**
     * @override
     */
    start: function () {
        this.class_name = this.$el.attr("class");
        this.item_template = this.$el.attr("data-item_template");
        this.owl_item_mobile = parseInt(this.$el.attr("data-owl_item_mobile")) || 1;
        this.owl_item_tablet = parseInt(this.$el.attr("data-owl_item_tablet")) || 3;
        this.owl_item_desktop = parseInt(this.$el.attr("data-owl_item_desktop")) || 5;
        this.categs_ids = [];

        //get selected categories
        var class_name = this.$el.attr("class");
        if (class_name) {
            //for category
            var categs_ids = [];
            var myStringArray = class_name.split(" ");
            var arrayLength = myStringArray.length;
            for (var i = 0; i < arrayLength; i++) {
                var js_categ_id = myStringArray[i].match("sh_categ_snipp_(.*)_cend");
                if (js_categ_id && js_categ_id.length == 2) {
                    categs_ids.push(parseInt(js_categ_id[1]));
                }
            }
            this.categs_ids = categs_ids;
        }

        this.KeepLast.add(this._fetch()).then(this._render.bind(this));
        return this._super.apply(this, arguments);
    },

    destroy: function () {
        this._super(...arguments);
        this.$el.find('.js_cls_our_partner_category_render_area').empty();
    },

    /**
     * @private
     */
    _fetch: function (values) {
        // Add dynamic content
        return rpc("/sh_corpomate_theme/our_partner_get_categories", {
            "item_template": this.item_template,
            "categs_ids": this.categs_ids,
        }).then((res) => {
            return res;
        });
    },

    /**
     * @private
     */
    _render: function (res) {
        // Add dynamic content
        this.$(".js_cls_our_partner_category_render_area").html(res.data);

        //refresh the owl start here
        this.$(".owl-carousel").owlCarousel({
            autoplay: true,
            autoplayTimeout: 5000,
            loop: true,
            nav: true,
            margin: 10,
            items: 4,
            navigation: true,
            responsive: {
                0: {
                    items: this.owl_item_mobile,
                    nav: true,
                },
                760: {
                    items: this.owl_item_tablet,
                    nav: false,
                },
                1000: {
                    items: this.owl_item_desktop,
                    nav: true,
                },
            },
        });
        this.$(".owl-carousel.js_cls_testimonial_onemate_2").owlCarousel({
            autoplay: true,
            autoplayTimeout: 5000,
            loop: true,
            nav: true,
            margin: 10,
            items: 4,
            navigation: true,
            responsive: {
                0: {
                    items: this.owl_item_mobile,
                    // nav: true,
                },
                760: {
                    items: this.owl_item_tablet,
                    // nav: false,
                },
                1000: {
                    items: this.owl_item_desktop,
                    // nav: true,
                },
            },
        });
    },

});