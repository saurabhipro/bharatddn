/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { KeepLast } from "@web/core/utils/concurrency";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.sh_testimonal_snippet_custom_js = publicWidget.Widget.extend({
  selector: ".js_cls_get_testimonial_custom",
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
    this.item_template = this.$el.attr("data-item_template") || false;
    this.owl_item_desktop = this.$el.attr("data-owl_item_desktop") || 3;
    this.owl_item_mobile = this.$el.attr("data-owl_item_mobile") || 1;
    this.owl_item_tablet = this.$el.attr("data-owl_item_tablet") || 3;

    this.KeepLast.add(this._fetch()).then(this._render.bind(this));
    return this._super.apply(this, arguments);
  },
  /**
   * @override
   */
  destroy: function () {
    this._super(...arguments);
    this.$el.find(".js_cls_render_dynamic_testimonial_area").html("");
  },

  //--------------------------------------------------------------------------
  // Private
  //--------------------------------------------------------------------------

  /**
   * @private
   */
  _fetch: function () {
    return rpc("/sh_testimonial_snippet/get_testimonial", {
      "item_template": this.item_template,
    }).then((res) => {
      return res;
    });
  },
  /**
   * @private
   */
  _render: function (res) {
    // Add dynamic content
    this.$(".js_cls_render_dynamic_testimonial_area").html(res.data);

    var is_rtl_enabled = $('#wrapwrap').hasClass('o_rtl');
    this.$(".owl-carousel").owlCarousel({
      items: this.owl_item_desktop,
      rtl: is_rtl_enabled,
      autoplay: false,
      loop: true,
      nav: true,
      margin: 10,
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
    var swiper = new Swiper(".js_cls_custom_swiper", {

      effect: "coverflow",
      grabCursor: true,
      centeredSlides: true,
      coverflowEffect: {
        rotate: 0,
        stretch: 0,
        depth: 100,
        modifier: 3,
        slideShadows: true,
        autoplay: 5000,
        speed: 1000
      },
      autoplay: true,
      loop: true,
      autoplay: {
        delay: 3000,
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true
      },
      breakpoints: {
        640: {
          slidesPerView: 1
        },
        768: {
          slidesPerView: 2
        },
        1024: {
          slidesPerView: 2
        },
        1560: {
          slidesPerView: 2
        }
      }
    });
  },
});
