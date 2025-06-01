/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import animations from "@website/js/content/snippets.animation";
import { cookie } from "@web/core/browser/cookie";


publicWidget.registry.sh_corpomate_zoom_toggle = animations.Animation.extend({
    selector: "#wrapwrap",
    events: {
        'click .js_cls_zoom_toggle_btn.zoom_in': '_click_expand_button',
        'click .js_cls_zoom_toggle_btn.zoom_out': '_click_compress_button',
        'click .js_cls_dark_mode':'_onClickDarkModeToggle',
    },

    _click_expand_button: function (ev) {
        ev.preventDefault();
        var self = this;
        $('.js_cls_zoom_toggle_btn.zoom_in').addClass('d-none');
        $('.js_cls_zoom_toggle_btn.zoom_out').removeClass('d-none');
        var elem = document.querySelector('body');
        if (elem.requestFullscreen) {
            elem.requestFullscreen();
        } else if (elem.mozRequestFullScreen) { /* Firefox */
            elem.mozRequestFullScreen();
        } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
            elem.webkitRequestFullscreen();
        } else if (elem.msRequestFullscreen) { /* IE/Edge */
            elem.msRequestFullscreen();
        }
    },
    _click_compress_button: function (ev) {
        ev.preventDefault();
        var self = this;
        $('.js_cls_zoom_toggle_btn.zoom_in').removeClass('d-none');
        $('.js_cls_zoom_toggle_btn.zoom_out').addClass('d-none');
        var elem = document.querySelector('body');
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.mozCancelFullScreen) { /* Firefox */
            document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) { /* Chrome, Safari and Opera */
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) { /* IE/Edge */
            document.msExitFullscreen();
        }
    },

    // Dark mode on off button toggle //
    _onClickDarkModeToggle : function(ev){
        var self = this;
        var corpomateDarkMode = window.location.hostname + "corpomateDarkMode";
        var current_mode = cookie.get(corpomateDarkMode) || "dark_mode_is_off";
        var is_dark_mode = current_mode === "dark_mode_is_on";

        var new_mode = is_dark_mode ? "dark_mode_is_off" : "dark_mode_is_on";
        var icon_content = is_dark_mode
            ? "<div class='dark_mode_inner dark_on_mode_inter_wrapper js_cls_dark_mode' title='Enable Dark Mode'>" +
            "<i class='fa fa-moon-o'></i>" +
            "</div>"
            : "<div class='dark_mode_inner dark_off_mode_inter_wrapper js_cls_dark_mode' title='Disable Dark Mode'>" +
            "<i class='fa fa-sun-o'></i>" +
            "</div>";

        cookie.set(corpomateDarkMode, new_mode, { expires: null });

        self.$el.toggleClass('dark_mode_is_on', !is_dark_mode);
        self.$el.toggleClass('dark_mode_is_off', is_dark_mode);
        self.$el.find('.dark_mode_inner').replaceWith(icon_content);
    },
});


publicWidget.registry.sh_corpomate_bottom_navbar = animations.Animation.extend({
    selector: "#wrapwrap",
    disabledInEditableMode: true,

    effects: [{
        startEvents: 'scroll',
        update: '_add_remove_top_to_bottom_navbar',
    }],



    /**
     * @constructor
     */
    init: function () {
        this._super(...arguments);
        var self = this;
        this.amount_scrolled = 300;


    },



    //--------------------------------------------------------------------------
    /**
     * Called when the window is scrolled
     *
     * @private
     * @param {integer} scroll
     */
    _add_remove_top_to_bottom_navbar: function (scroll) {
        var self = this;
        const navbar = $(document).find('.js_cls_bottom_nav_bar_wrapper');
        const $footer = document.querySelector('footer');
        if($footer != null){
            const footerRect = $footer.getBoundingClientRect();
            if (navbar.length > 0 && footerRect.top <= window.innerHeight) {
                navbar.fadeOut('slow');
            } else {
                navbar.fadeIn('slow');
            }
        }

    },
});




publicWidget.registry.sh_corpomate_bottom_navbar_sh_corpomate_theme_section_536 = animations.Animation.extend({
    selector: "#sh_corpomate_theme_section_536",
    disabledInEditableMode: true,

    effects: [{
        startEvents: 'scroll',
        update: '_on_scroll_animation',
    }],


    //--------------------------------------------------------------------------
    /**
     * Called when the window is scrolled
     *
     * @private
     * @param {integer} scroll
     */
    _on_scroll_animation: function (scroll) {
        var self = this;

        var scrollValue = self.$el.find('.js_cls_scroll_animation').scrollTop();
        var winWdith = $(window).width();
    },


});

// sh_corpomate_theme_crypto_7 start//
$(document).ready(function () {

    $('[data-bs-toggle="popover"]').popover();
});
$(document).find('.js_cls_sh_corpomate_theme_flag_btn').click(function () {
    $(document).find(".sh_bottom_nav  #sh_corpomate_lang_dropdown_area").slideToggle('slow')

})





$("#sh_corpomate_theme_crypto_7 .testimonial .indicators li").click(function () {
    var i = $(this).index();
    var targetElement = $(".testimonial .tabs li");
    targetElement.eq(i).addClass('active');
    targetElement.not(targetElement[i]).removeClass('active');
});
$("#sh_corpomate_theme_crypto_7 .testimonial .tabs li").click(function () {
    var targetElement = $(".testimonial .tabs li");
    targetElement.addClass('active');
    targetElement.not($(this)).removeClass('active');
});
$("#sh_corpomate_theme_crypto_7 .slider .swiper-pagination span").each(function (i) {
    $(this).text(i + 1).prepend("0");
});
// sh_corpomate_theme_crypto_7 end//

$(document).find(".sh_header_custom_1 .header_1 > a").click(function (ev) {
    var $shareBtn = $(ev.currentTarget)
    $shareBtn.toggleClass('header_1_links');
    $shareBtn.next('.header_link_share').slideToggle('slow', function () {
        if ($('.header_link_share').is(':hidden')) {
            $('.header_link_share').addClass('arrow_animation')
        }
        else {
            $('.header_link_share').removeClass('arrow_animation')
        }
    })
});


// sh_corpomate_theme_accounting_6 start//

$('#sh_corpomate_theme_accounting_6 .sh_testimonial_links img#link_1').click(function (ev) {
    $('#sh_corpomate_theme_accounting_6 .sh_testimonial_links img').removeClass('active')

    var $img = $(ev.currentTarget);
    $img.addClass('active');
    $('#sh_corpomate_theme_accounting_6 .sh_testimonial_custom #link_1').click()
})

$('#sh_corpomate_theme_accounting_6 .sh_testimonial_links img#link_2').click(function (ev) {
    $('#sh_corpomate_theme_accounting_6 .sh_testimonial_links img').removeClass('active')

    var $img = $(ev.currentTarget);
    $img.addClass('active');
    $('#sh_corpomate_theme_accounting_6 .sh_testimonial_custom #link_2').click()
})

$('#sh_corpomate_theme_accounting_6 .sh_testimonial_links img#link_3').click(function (ev) {
    $('#sh_corpomate_theme_accounting_6 .sh_testimonial_links img').removeClass('active')

    var $img = $(ev.currentTarget);
    $img.addClass('active');
    $('#sh_corpomate_theme_accounting_6 .sh_testimonial_custom #link_3').click()
})

$('#sh_corpomate_theme_accounting_6 .sh_testimonial_links img#link_4').click(function (ev) {
    $('#sh_corpomate_theme_accounting_6 .sh_testimonial_links img').removeClass('active')

    var $img = $(ev.currentTarget);
    $img.addClass('active');
    $('#sh_corpomate_theme_accounting_6 .sh_testimonial_custom #link_4').click()
})

$('#sh_corpomate_theme_accounting_6 .sh_testimonial_links img#link_5').click(function (ev) {
    $('#sh_corpomate_theme_accounting_6 .sh_testimonial_links img').removeClass('active')

    var $img = $(ev.currentTarget);
    $img.addClass('active');
    $('#sh_corpomate_theme_accounting_6 .sh_testimonial_custom #link_5').click()
})


// sh_corpomate_theme_accounting_6 end//

$('#sh_corpomate_theme_section_561 .sh_box .js_cls_carousel_link_content').click(function (ev) {
    var $link = $(ev.currentTarget);
    var content = $link.find('img').attr('class');
    if (content) {
        $('#sh_corpomate_theme_section_561 .sh_testimonial_custom .carousel-item').removeClass('active');
        $('#sh_corpomate_theme_section_561 .carousel-indicators li').removeClass('active');
        $('#sh_corpomate_theme_section_561 .carousel-indicators').find('.' + content).addClass('active');
        $('#sh_corpomate_theme_section_561 .sh_testimonial_custom').find('.' + content).addClass('active');
    }
});

//hide admin authentication
$($('.nav-item.dropdown.o_no_autohide_item')[0]).addClass('sh-show-auth-mobile')





// On click menuitem


// $(document).on('click', 'header a.nav-link, header a.dropdown-item, #sh_footer6 .sh_footer_menu a', function (e) {
//     var href = $(this).attr('href');
//     console.log('log ==>> href ====',href);
//     // Remove active class from all menu links
//     $('header a.nav-link, header a.dropdown-item, #sh_footer6 .sh_footer_menu a').removeClass('active');

//     if (href.includes("#")) {
//         e.preventDefault(); // Prevent default anchor behavior
//         href = href.replace(/^\/?#\/?/, '');
//         var targetElement = $(href);
//         if (targetElement.length) {
//             console.log('log ==>> Onemate',);

//             $("header").find('a.active').removeClass('active');
//             $(this).addClass('active');
//             $('.navbar-collapse').collapse('hide');
//             var basescrollLocation = targetElement.offset().top;
//             var scrollLocation = basescrollLocation;

//             // Adjust for the navbar height
//             var navbarHeight = $('.o_main_navbar').height() || 0;
//             if (navbarHeight) {
//                 scrollLocation -= navbarHeight;
//             }

//             // Adjust for the header height
//             var headerHeight = $('.o_header_standard').height() || 0;
//             if (headerHeight) {
//                 scrollLocation -= headerHeight;
//             }

//             var scrollinside = $("#wrapwrap").scrollTop();
//             $('#wrapwrap').animate({
//                 scrollTop: scrollinside + scrollLocation
//             }, 500);

//             // $('html, body').animate({
//             //     scrollTop: targetElement.offset().top
//             // }, 800); // 800ms smooth scrolling
//         }

//         // Add active class to clicked link
//         $(this).addClass('active');
//     } else {
//         // Allow normal page redirection
//         console.log('log ==>> RATHER Onemate',);
//         window.location.href = href;
//     }
// });






$(document).on('click', 'header a.nav-link, header a.dropdown-item, #sh_footer6 .sh_footer_menu a', function (e) {
    var href = $(this).attr("href");
    console.log("\n\n href == href",href)
    // Ignore if the href is '#' or if it starts with 'tel:'
    if (!href || href === '#' || href.startsWith('tel:')) {
        console.log("\n\n href == 111")
        return;
    }

    // Process the href to remove leading slashes or hashes


    // Ignore if href starts with '/'
    // if (href.startsWith('/')) {
    //     console.log("\n\n href == 222")
    //     return;
    // }
    console.log("\n\n href == href",href)
    // Proceed with scrolling if the target exists
    if (href.includes("#") ) {
        e.preventDefault();
        href = href.replace(/^\/?#\/?/, '');
        console.log("\n\n href == href",href)
        var $target = $("#"+href);
        console.log("\n\n href == $target",$target)
        if ($target.length) {
            // Manage active class for the clicked link
            $("header").find('a.active').removeClass('active');
            $(this).addClass('active');

            $('.navbar-collapse').collapse('hide');

            var basescrollLocation = $target.offset().top;
            var scrollLocation = basescrollLocation;

            // Adjust for the navbar height
            var navbarHeight = $('.o_main_navbar').height() || 0;
            if (navbarHeight) {
                scrollLocation -= navbarHeight;
            }

            // Adjust for the header height
            var headerHeight = $('.o_header_standard').height() || 0;
            if (headerHeight) {
                scrollLocation -= headerHeight;
            }
            console.log('log ==>> $target',$target);
            $('html, body').animate({
                scrollTop: $target.offset().top - 100
            }, 800);

        }
    }
//    else{
//        console.log("\n\n href == REDIRECTS")
//        window.location.href = href;
//    }
});







// $(document).on('click', 'header a.nav-link, header a.dropdown-item, #sh_footer6 .sh_footer_menu a', function (e) {
// 	// $('#wrapwrap').stop().animate({


// 	// });



// 	var href = $(this).attr("href");

// 	if (href === '#') {
// 		return;
// 	}

// 	if (href) {
// 		var href = href.substring(href.indexOf('/#') + 1);
// 	}

// 	if (href && href.startsWith('/#') ) {
// 	    href = href.replace('/', '');
// 	}

// 	if (href && href.startsWith('/')) {
// 		return;
// 	}

// 	//e.preventDefault();
// 	//e.stopPropagation();

//     var href_formated = href.replace('tel://','')
//     var $target = $(href_formated);

// 	if ($target.length) {
// 		//TODO: active or inactive class in menu if possible.

// 		// active or inactive
// 		$("header").find('a.active').removeClass('active');
// 		$(this).addClass('active');

// 		$('.navbar-collapse').collapse('hide');

// 		var basescrollLocation = $target.offset().top;
// 		var scrollLocation = basescrollLocation;

// 		// navbar
// 		var navbarHeight = $('.o_main_navbar').height() || 0;
// 		if (navbarHeight) {
// 			// In overflow auto, scrollLocation of target can be negative if target is out of screen (up side)
// 			scrollLocation = basescrollLocation >= 0 ? basescrollLocation - navbarHeight : basescrollLocation - navbarHeight;
// 		}

// 		// header
// 		var headerHeight = $('.o_header_standard').height() || 0;
// 		var headerscrollLocation = 0;
// 		if (headerHeight) {
// 			// In overflow auto, scrollLocation of target can be negative if target is out of screen (up side)
// 			scrollLocation = basescrollLocation >= 0 ? scrollLocation - headerHeight : scrollLocation - headerHeight;
// 		}

// 		//			var scrolltoOffset =  $('main').offset().top + ( $('header').offset().top || 46 );
// 		var scrollinside = $("#wrapwrap").scrollTop();
//         $('#wrapwrap').animate({
//             scrollTop: scrollinside + scrollLocation
//         }, 500);
// 	}



// });


