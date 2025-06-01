/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import animations from "@website/js/content/snippets.animation";
import { AssetsLoadingError, loadJS } from '@web/core/assets';

// Wait for the AOS library to be available before initializing
publicWidget.registry.sAnimationWidget = animations.Animation.extend({
    selector: ".aos-init",
    disabledInEditableMode: true,
    effects: [
        {
            startEvents: "scroll",
            update: "_updateCounterOnScroll",
        },
    ],

    /**
     * @constructor
     */
    init: function () {
        this._super(...arguments);

        try {
            const loadBoot = Promise.all([
                loadJS('https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.js'),
            ])
        } catch (error) {
            if (!(error instanceof AssetsLoadingError)) {
                throw error;
            }
        }

        setTimeout(() => {
            // Ensure AOS is loaded and available
            if (typeof AOS !== 'undefined') {
                this.AOS = AOS.init({});
            } else {
                console.error('AOS library not loaded!');
            }
        }, 3000);

        
    }, 

    //----------------------------------------------------------------------
    // Handlers
    //----------------------------------------------------------------------
    /**
     * Called when the window is scrolled
     *
     * @private
     * @param {integer} scroll
     */
    _updateCounterOnScroll: function (scroll) {
        if (this.isElementPartiallyInViewport(this.$el)) {
            this.$el.addClass("aos-animate");
        } else {
            this.$el.removeClass("aos-animate");
        }
    },

    isElementPartiallyInViewport(el) {
        // Special bonus for those using jQuery
        if (typeof jQuery !== "undefined" && el instanceof jQuery) el = el[0];
    
        var rect = el.getBoundingClientRect();
        var windowHeight = window.innerHeight || document.documentElement.clientHeight;
        var windowWidth = window.innerWidth || document.documentElement.clientWidth;
    
        var vertInView = rect.top <= windowHeight && rect.top + rect.height >= 0;
        var horInView = rect.left <= windowWidth && rect.left + rect.width >= 0;
    
        return vertInView && horInView;
    }
});


// import publicWidget from "@web/legacy/js/public/public_widget";
// import animations from "@website/js/content/snippets.animation";

// publicWidget.registry.sAnimationWidget = animations.Animation.extend({
//     selector: ".aos-init",
//     disabledInEditableMode: true,
//     effects: [
//         {
//             startEvents: "scroll",
//             update: "_updateCounterOnScroll",
//         },
//     ],

//     /**
//      * @constructor
//      */
//     init: function () {
//         this._super(...arguments);
//         this.AOS = AOS.init({});
//     }, 

//     //--------------------------------------------------------------------------
//     // Handlers
//     //--------------------------------------------------------------------------
//     /**
//      * Called when the window is scrolled
//      *
//      * @private
//      * @param {integer} scroll
//      */
//     _updateCounterOnScroll: function (scroll) {
//         if (this.isElementPartiallyInViewport(this.$el)) {
//             this.$el.addClass("aos-animate");
//         } else {
//             this.$el.removeClass("aos-animate");
//         }
//     },
//     isElementPartiallyInViewport(el) {
//         // Special bonus for those using jQuery
//         if (typeof jQuery !== "undefined" && el instanceof jQuery) el = el[0];
    
//         var rect = el.getBoundingClientRect();
//         // DOMRect { x: 8, y: 8, width: 100, height: 100, top: 8, right: 108, bottom: 108, left: 8 }
//         var windowHeight = window.innerHeight || document.documentElement.clientHeight;
//         var windowWidth = window.innerWidth || document.documentElement.clientWidth;
    
//         // http://stackoverflow.com/questions/325933/determine-whether-two-date-ranges-overlap
//         var vertInView = rect.top <= windowHeight && rect.top + rect.height >= 0;
//         var horInView = rect.left <= windowWidth && rect.left + rect.width >= 0;
    
//         return vertInView && horInView;
//     }
// });