/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { KeepLast } from "@web/core/utils/concurrency";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.sh_blog_filter_snippet_s_post = publicWidget.Widget.extend({
    selector: ".js_cls_get_sh_blog_filter_s_post",
    disabledInEditableMode: true,
    read_events: {
        "click .js_cls_tab_a": "_onClickTab",
    },

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
        this.item_template = this.$el.attr("data-item_template") || false;
        this.column_class = this.$el.attr("data-column_class") || "col-md-4";
        this.owl_item_mobile = this.$el.attr("data-owl_item_mobile") || 1;
        this.owl_item_tablet = this.$el.attr("data-owl_item_tablet") || 3;
        this.single_tab_item_template = this.$el.attr("data-single_tab_item_template") || false;
        this.order = this.$el.attr("data-order") || "";
        this.limit = parseInt(this.$el.attr("data-limit")) || false;
        this.blogs_ids = [];
        this.filter_id = parseInt(this.$el.data("filterId")) || false;

        //get snippet options
        var className = this.$el.attr("class");
        if (className) {
            //for category
            var blogs_ids = [];
            var classArray = className.split(" ");
            var arrayLength = classArray.length;
            for (var i = 0; i < arrayLength; i++) {
                var js_blog_id = classArray[i].match("sh_blog_(.*)_bend");
                if (js_blog_id && js_blog_id.length == 2) {
                    blogs_ids.push(parseInt(js_blog_id[1]));
                }
            }
            this.blogs_ids = blogs_ids;
        }

        this.KeepLast.add(this._fetch()).then(this._render.bind(this));
        return this._super.apply(this, arguments);
    },
    /**
     * @override
     */
    destroy: function () {
        this._super(...arguments);
        this.$el.find(".js_cls_render_dynamic_post_area").html("");
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _fetch: function () {
        var loading = '<i class="js_cls_tab_pane_loading fa fa-circle-o-notch fa-spin" style="font-size:80px;width:100%;text-align:center;"></i>';

        this.$el.find(".js_cls_render_dynamic_post_area").append(loading);

        return rpc("/sh_blog_filter_snippet/get_posts", {
            "item_template": this.item_template,
            "blogs_ids": this.blogs_ids,
            "filter_id": this.filter_id,
            "options": {
                order: this.order,
                limit: this.limit,
                column_class: this.column_class,
            },
        }).then((res) => {
            return res;
        });
    },
    /**
     * @private
     */
    _render: function (res) {
        // Add dynamic content
        this.$(".js_cls_render_dynamic_post_area").html(res.data);

        //refresh owl
        if (res.is_show_slider_local) {
            var is_rtl_enabled = $('#wrapwrap').hasClass('o_rtl');
            this.$(".js_cls_tab_pane_content").owlCarousel({
                items: 4,
                rtl: is_rtl_enabled,
                autoplay: true,
                loop: true,
                navigation: true,
                responsive: {
                    0: {
                        items: this.owl_item_mobile,
                    },
                    600: {
                        items: this.owl_item_tablet,
                    },
                    1000: {
                        items: res.items,
                    },
                },
            });
        }
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * Add product to cart and reload the carousel.
     * @private
     * @param {Event} ev
     */
    _onClickTab: function (ev) {
        var self = this;
        var tab_pane_id = $(ev.currentTarget).attr("href");
        var tab_id = parseInt($(ev.currentTarget).attr("data-tab_id")) || false;
        var $tab_pane_content = self.$el.find(tab_pane_id).find(".js_cls_tab_pane_content");
        var is_data_loaded = $tab_pane_content.attr("data-loaded");
        if (is_data_loaded) {
            return;
        }

        var loading = '<i class="js_cls_tab_pane_loading fa fa-circle-o-notch fa-spin" style="font-size:80px;width:100%;text-align:center;"></i>';
        var $already_loading = $tab_pane_content.find(".js_cls_tab_pane_loading");
        if ($already_loading.length) {
            $already_loading.replaceWith(loading);
        } else {
            $tab_pane_content.prepend(loading);
        }

        rpc("/sh_blog_filter_snippet/get_posts", {
            "item_template": this.single_tab_item_template,
            "blogs_ids": this.blogs_ids,
            "filter_id": this.filter_id,
            "options": {
                order: this.order,
                limit: this.limit,
                tab_id: tab_id,
                column_class: this.column_class,
            },
        }).then(function (res) {
            $tab_pane_content.html(res.data);
            $tab_pane_content.attr("data-loaded", true);
            //refresh owl
            if (res.is_show_slider_local) {
                var is_rtl_enabled = $('#wrapwrap').hasClass('o_rtl');
                $tab_pane_content.owlCarousel("destroy");
                $tab_pane_content.owlCarousel({
                    items: res.items,
                    rtl: is_rtl_enabled,
                    autoplay: res.autoplay,
                    speed: res.speed,
                    loop: res.loop,
                    nav: res.nav,
                    responsive: {
                        0: {
                            items: self.owl_item_mobile,
                        },
                        600: {
                            items: self.owl_item_tablet,
                        },
                        1000: {
                            items: res.items,
                        },
                    },
                });
            }
        });
    },
});
