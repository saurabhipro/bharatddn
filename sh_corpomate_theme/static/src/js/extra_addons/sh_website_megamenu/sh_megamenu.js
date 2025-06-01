/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

import { rpc } from '@web/core/network/rpc';
import { renderToElement } from "@web/core/utils/render";
import { KeepLast } from "@web/core/utils/concurrency";


const { markup } = owl;





publicWidget.registry.sh_website_megamenu_s_megamenu = publicWidget.Widget.extend({
    selector: ".js_cls_get_sh_w_megamenu_content",
    disabledInEditableMode: true,

    /**
     * @constructor
     */
    init: function () {
        this._super.apply(this, arguments);
        this.keepLast = new KeepLast();
    },

    /**
     * @constructor
     */
    // init: function () {
    //     this._super.apply(this, arguments);
    //     this._dp = new concurrency.DropPrevious();
    // },
    /**
     * @override
     */
    start: function () {
        this.item_template = this.$el.attr("data-item_template") || false;
        this.categs_ids = [];
        this.filter_id = parseInt(this.$el.data("filterId")) || false;

        this.keepLast.add(this._fetch()).then(this._render.bind(this));
        return this._super.apply(this, arguments);
    },
    /**
     * @override
     */
    destroy: function () {
        this._super(...arguments);
        this.$el.find(".js_cls_render_dynamic_content_area").html("");
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------


    /**
     * @private
     */
    _fetch: function () {
        return rpc("/sh_website_megamenu/get_content", {
            'item_template': this.item_template,
            'filter_id': this.filter_id
        }).then((res) => {
            return res;
        });
    },
    /**
     * @private
     */
    _render: function (res) {
        // Add dynamic content
        this.$(".js_cls_render_dynamic_content_area").html(res.data);
    },
});
