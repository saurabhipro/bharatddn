/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { KeepLast } from "@web/core/utils/concurrency";
import { rpc } from "@web/core/network/rpc";
import { AssetsLoadingError, loadCSS, loadJS } from '@web/core/assets';

publicWidget.registry.shOnematePortfolio = publicWidget.Widget.extend({
    selector: '.js_cls_get_sh_onemate_s_portfolio',
    disabledInEditableMode: true,
    read_events: {
        'click .js_cls_s_portfolio_filter_button': '_onClickFilterButton',
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
        this.item_template = this.$el.attr('data-item_template') || false;

        try {
            const loadBoot = Promise.all([
                loadJS('sh_corpomate_theme/static/src/libs/lc_lightbox/lc_lightbox.lite.js'),
                // loadCSS('https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css'),
            ])
            console.log('log ==>> LOAD JS lc_lightbox',loadBoot);
        } catch (error) {
            console.log('log ==>> LOAD JS lc_lightbox',error);
            if (!(error instanceof AssetsLoadingError)) {
                throw error;
            }
        }
        setTimeout(function () {
            console.log('log ==>> lc_lightbox');
            // this.initialize_lc_lightbox();

            lc_lightbox('.js_cls_s_portfolio_lcl', {
                wrap_class: 'lcl_fade_oc',
                gallery: true,
                thumb_attr: 'data-lcl-thumb',
                skin: 'dark',
                radius: 0,
                padding: 0,
                border_w: 0,
            });
        }, 2000);
        
        this.KeepLast.add(this._fetch()).then(this._render.bind(this));
        return this._super.apply(this, arguments);

    },

    /**
     * Initialize LC Lightbox plugin.
     * @private
     */
    initialize_lc_lightbox: function () {

        lc_lightbox('.js_cls_s_portfolio_lcl', {
            wrap_class: 'lcl_fade_oc',
            gallery: true,
            thumb_attr: 'data-lcl-thumb',
            skin: 'dark',
            radius: 0,
            padding: 0,
            border_w: 0,
        });
    },


    /**
     * @override
     */
    destroy: function () {
        this._super(...arguments);
        this.$el.find('.js_cls_render_dynamic_portfolio_area').html('');
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _fetch: function () {
        return rpc('/sh_onemate_theme/get_portfolio', {
            'item_template': this.item_template,
        }).then(res => {
            return res;
        });
    },
    /**
     * @private
     */
    _render: function (res) {
        // Add dynamic content
        this.$('.js_cls_render_dynamic_portfolio_area').html(res);
    },


    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * Add product to cart and reload the carousel.
     * @private
     * @param {Event} ev
     */
    _onClickFilterButton: function (ev) {
        var self = this;
        var $button = $(ev.currentTarget);
        var value = $button.attr('data-filter');
        self.$el.find(".js_cls_s_portfolio_filter_button").removeClass("active");
        $button.addClass("active");

        if (value == "all") {
            self.$el.find('.js_cls_s_portfolio_filter_el').show('1000');
        }
        else {
            self.$el.find(".js_cls_s_portfolio_filter_el").not('.' + value).hide('3000');
            self.$el.find('.js_cls_s_portfolio_filter_el').filter('.' + value).show('3000');
        }
    },




});

