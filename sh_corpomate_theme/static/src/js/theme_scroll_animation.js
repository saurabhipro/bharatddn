/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import animations from "@website/js/content/snippets.animation";
    
    
publicWidget.registry.shOnemateHeaderHighlightWidget = animations.Animation.extend({
    selector: '#wrap > section',	
    disabledInEditableMode: true,
    effects: [{
        startEvents: 'scroll',
        update: '_updateNavItemOnScroll',
    }],

    /**
     * @constructor
     */
    init: function () {    	
        this._super(...arguments);
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------
    /**
     * Called when the window is scrolled
     *
     * @private
     * @param {integer} scroll
     */
    _updateNavItemOnScroll: function (scroll) {    	
        
        // navbar
        var navbarHeight = $('.o_main_navbar').height() || 0;        
        // header
        var headerHeight = $('.o_header_standard').height() || 0;

        
        var cur_pos = $(window).scrollTop() + 200;
        
            var top = this.$el.offset().top - navbarHeight - headerHeight,
            bottom = top + this.$el.outerHeight();
            
            if (cur_pos >= top && cur_pos <= bottom) {            
                if (location.hash || window.location.pathname === '/' || window.location.pathname === $("ul#top_menu").find('a:first').attr('href') ){
                    if (cur_pos <= bottom) {

                        $("header.o_header_affixed").find('a.active').removeClass('active');
                    }
                    $("header.o_header_affixed").find('a[href="/#' + this.$el.attr('id') + '"]').addClass('active');
                }
            
            }



        
    },

});
