# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Corpomate Theme - Multipurpose Corporate Theme",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "suppport@softhealer.com",
    'category': 'Themes/Corporate',
    "license": "OPL-1",
    "summary": "Corporate Theme Construction Theme Medical Theme Finance Theme Business Theme SaaS Theme Digital Mobile App Web App Creative Corporate Theme Multipurpose Theme Pet Care Theme salon Theme Industry Theme Laboratory Theme agriculture Theme NGO Theme Fitness Theme Law Theme Transportation Theme Attractive corporate website Customizable corporate website Futuristic corporate website Responsive corporate website Clean theme Attractive corporate Theme Customizable Website Theme Professional Corporate Theme Odoo",
    "description": """
	Hey! Are you looking for Attractive, Customizable, Futuristic, Responsive, Clean theme for your corporate website in odoo? Here it is! In this theme you will get 8 different pre-designed theme style or it will customise as required. This theme builds with designs and various features like Mega menu, cookie notice, news bar, Snippet builder, Website Comming Soon as well as is a Modern & custom odoo theme. It will design with bootstrap so it will be suitable for kinds of the corporate websites. In this theme, all features will be suitable for the multi-website in odoo. It is a fully responsive theme and looks equally stunning on all kinds of screens and devices. Corpomate theme is a clear and feature stuffed theme for the odoo website.
                    """,
    "version": "0.0.4",
    "depends": [
        "website_crm",
        "mass_mailing",
        "website_blog",
        "web_editor",
        "website_sale",
    ],
    "application": True,
    "data": [
        "security/notice_board_security.xml",
        "security/ir.model.access.csv",
        "data/demo_data/corpomate_demo.xml",
        "views/copyright.xml",
        "views/readymade.xml",
        "views/topbar.xml",
        "views/footer_view.xml",
        "views/header.xml",
        "views/color.xml",
        "views/font.xml",
        "views/theme_options.xml",

        # DYNAMIC BLOG SNIPPETS
        "views/s_button.xml",
        "views/snippets/theme_1_s.xml",
        "views/snippets/theme_2_s.xml",
        "views/snippets/theme_3_s.xml",
        "views/snippets/theme_4_s.xml",
        "views/snippets/theme_5_s.xml",
        "views/snippets/theme_6_s.xml",
        "views/snippets/onemate_portfolio_s.xml",        
        "views/snippets.xml",
        "views/testimonial_templates.xml",
        "views/our_partner_templates.xml",
        "views/testimonial_view.xml",
        "views/our_partners_view.xml",
        "views/our_partners_category_views.xml",
        "views/website_views.xml",

        # THEME 1
        "views/pages/about_us/page_about_us_1.xml",
        "views/pages/home/page_home_1.xml",
        "views/pages/service/page_service_1.xml",
        "views/pages/contact_us/page_contact_us_1.xml",
        "views/pages/our_team/page_our_team_1.xml",

        # THEME 2
        "views/pages/about_us/page_about_us_2.xml",
        "views/pages/home/page_home_2.xml",
        "views/pages/service/page_service_2.xml",
        "views/pages/contact_us/page_contact_us_2.xml",

        # THEME 3
        "views/pages/about_us/page_about_us_3.xml",
        "views/pages/home/page_home_3.xml",
        "views/pages/service/page_service_3.xml",
        "views/pages/contact_us/page_contact_us_3.xml",
        "views/pages/project/project_3.xml",
        "views/pages/gallery/page_gallery_3.xml",


        # THEME 4
        "views/pages/about_us/page_about_us_4.xml",
        "views/pages/home/page_home_4.xml",
        "views/pages/service/page_service_4.xml",
        "views/pages/contact_us/page_contact_us_4.xml",
        "views/pages/portfolio/page_portfolio_4.xml",
        "views/pages/our_team/page_our_team_4.xml",

         # THEME 5
        "views/pages/home/page_home_5.xml",

         # THEME 6
        "views/pages/home/page_home_6.xml",


        # Bottom Navigation Bar
        "data/demo_data/bottom_nav_bar.xml",
        "views/bottom_nav_bar/bottom_nav_bar.xml",
        "views/res_config_settings.xml",
        "views/bottom_nav_bar/bottom_nav_bar_tmpl_style.xml",
        "views/bottom_nav_bar/bottom_nav_bar_tmpl.xml",

        # MENU
        "data/website_menu_1.xml",
        "data/website_menu_2.xml",
        "data/website_menu_3.xml",
        "data/website_menu_4.xml",
        "data/website_menu_5.xml",
        "data/website_menu_6.xml",

        # sh_blog_filter_snippet
        "extra_addons/sh_blog_filter_snippet/views/filter.xml",
        "extra_addons/sh_blog_filter_snippet/views/post_s_item.xml",
        "extra_addons/sh_blog_filter_snippet/views/post_s.xml",
        "extra_addons/sh_blog_filter_snippet/views/snippet_option.xml",
        "extra_addons/sh_blog_filter_snippet/views/snippet_panel.xml",

        # sh_cookie_notice
        "extra_addons/sh_cookie_notice/views/cookie_notice_template.xml",
        "extra_addons/sh_cookie_notice/views/res_config_settings_view.xml",
        "extra_addons/sh_cookie_notice/views/website_view.xml",

        # sh_html_snippet
        "extra_addons/sh_html_snippet/views/sh_html_snippet_templates.xml",
        "extra_addons/sh_html_snippet/views/website_templates.xml",

        # website_maintainance
        "extra_addons/website_maintainance/views/website_templates.xml",
        "extra_addons/website_maintainance/views/res_config_settings_views.xml",
        "extra_addons/website_maintainance/views/website_views.xml",

        # sh_website_popup
        "extra_addons/sh_website_popup/views/res_config_settings_views.xml",
        "extra_addons/sh_website_popup/views/website_templates.xml",
        "extra_addons/sh_website_popup/views/sh_website_popup_templates.xml",

        # sh_website_portfolio
        "extra_addons/sh_website_portfolio/data/sh_website_portfolio_demo.xml",
        "extra_addons/sh_website_portfolio/views/sh_website_portfolio_templates.xml",
        "extra_addons/sh_website_portfolio/views/website_portfolio_views.xml",

        # sh_notice_board
        "extra_addons/sh_notice_board/views/notice_board_view.xml",
        "extra_addons/sh_notice_board/views/snippets.xml",

        # sh_website_wtsapp
        "extra_addons/sh_website_wtsapp/data/res_config_settings_data.xml",
        "extra_addons/sh_website_wtsapp/views/res_config_settings_views.xml",
        "extra_addons/sh_website_wtsapp/views/website_views.xml",
        "extra_addons/sh_website_wtsapp/views/sh_website_wtsapp_templates.xml",

        # sh_website_quote
        "extra_addons/sh_website_quote/views/res_config_settings_views.xml",
        "extra_addons/sh_website_quote/views/website_views.xml",
        "extra_addons/sh_website_quote/views/website_templates.xml",

        # sh_website_coming_soon
        "extra_addons/sh_website_coming_soon/views/res_config_settings_view.xml",
        "extra_addons/sh_website_coming_soon/views/sh_website_coming_soon_templates.xml",

        # sh_pwa_frontend
        # "extra_addons/sh_pwa_frontend/views/sh_send_notifications.xml",
        # "extra_addons/sh_pwa_frontend/data/sh_firebase_notification_data.xml",
        # "extra_addons/sh_pwa_frontend/data/sh_pwa_configuraion_data.xml",
        # "extra_addons/sh_pwa_frontend/views/res_config_settings_views.xml",
        # "extra_addons/sh_pwa_frontend/views/sh_push_notification.xml",
        # "extra_addons/sh_pwa_frontend/views/sh_pwa_frontend_config_views.xml",


        # sh_web_push_notifications
        "extra_addons/sh_web_push_notifications/views/sh_send_notifications_views.xml",
        "extra_addons/sh_web_push_notifications/data/sh_push_notification_data.xml",
        "extra_addons/sh_web_push_notifications/views/res_config_settings_views.xml",
        "extra_addons/sh_web_push_notifications/views/sh_push_notification_views.xml",

        # sh_snippet_builder
        "extra_addons/sh_snippet_builder/data/sh_snippet_data.xml",
        "extra_addons/sh_snippet_builder/views/sh_snippet_builder_views.xml",
        "extra_addons/sh_snippet_builder/views/sh_snippet_template.xml",

        # sh_image_hotspot_snippet
        "extra_addons/sh_image_hotspot_snippet/data/sh_hotspot_snippet_demo.xml",
        "extra_addons/sh_image_hotspot_snippet/views/sh_image_hotpost_info_views.xml",
        "extra_addons/sh_image_hotspot_snippet/views/sh_image_snippet_templates.xml",
        "extra_addons/sh_image_hotspot_snippet/views/website_templates.xml",

        # sh_pwa_frontend
        # "extra_addons/sh_pwa_frontend/data/sh_firebase_notification_data.xml",
        # "extra_addons/sh_pwa_frontend/data/sh_pwa_configuraion_data.xml",
        # "extra_addons/sh_pwa_frontend/views/res_config_settings_views.xml",
        # "extra_addons/sh_pwa_frontend/views/sh_push_notification.xml",
        # "extra_addons/sh_pwa_frontend/views/sh_pwa_frontend_config_views.xml",
        # "extra_addons/sh_pwa_frontend/views/sh_send_notifications.xml",

        # sh_snippet_adv
        "extra_addons/sh_snippet_adv/views/web_editor.xml",

        # sh_website_preloader
        "extra_addons/sh_website_preloader/views/res_config_settings_view.xml",

        # sh_website_store_locator
        "extra_addons/sh_website_store_locator/data/sh_website_store_data.xml",
        "extra_addons/sh_website_store_locator/views/sh_website_store_locator_template.xml",
        "extra_addons/sh_website_store_locator/views/sh_website_store_locator_views.xml",
        "extra_addons/sh_website_store_locator/views/sh_website_store_tags_views.xml",
        "extra_addons/sh_website_store_locator/views/website_views.xml",

        ## sh_website_megamenu
        "views/website_menu_views.xml",
        "views/sh_menu_templates.xml",
        "views/product_public_category_views.xml",
        "views/sh_mega_menu_config_views.xml",
        "views/snippets/sh_s_item.xml",
        "views/snippets/s_options.xml",
        "views/snippets/snippets.xml",
    ],

    'assets': {
        'web.assets_frontend': [

            'sh_corpomate_theme/static/src/scss/as_mixin.scss',
            #'sh_corpomate_theme/static/src/scss/owl.carousel.css',
            # 'sh_corpomate_theme/static/src/scss/owl.theme.default.min.css',
            'sh_corpomate_theme/static/src/scss/variables.scss',
            'sh_corpomate_theme/static/src/scss/style.scss',
            'sh_corpomate_theme/static/src/scss/blog.scss',
            'sh_corpomate_theme/static/src/scss/event.scss',
            'sh_corpomate_theme/static/src/scss/job.scss',
            'sh_corpomate_theme/static/src/scss/help.scss',
            'sh_corpomate_theme/static/src/scss/animate.css',
            'sh_corpomate_theme/static/src/scss/bottom_nav_bar.scss',
            'sh_corpomate_theme/static/src/scss/theme/theme_1/theme_1_s.scss',
            'sh_corpomate_theme/static/src/scss/theme/theme_2/theme_2_s.scss',
            'sh_corpomate_theme/static/src/scss/theme/theme_3/theme_3_s.scss',
            'sh_corpomate_theme/static/src/scss/theme/theme_4/theme_4_s.scss',
            'sh_corpomate_theme/static/src/scss/theme/theme_5/theme_5_s.scss',
            'sh_corpomate_theme/static/src/scss/theme/theme_5/night_mode.scss',
            'sh_corpomate_theme/static/src/scss/theme/theme_6/theme_6_s.scss',
            'sh_corpomate_theme/static/src/scss/theme/theme_6/night_mode.scss',
            'sh_corpomate_theme/static/src/js/extra_addons/onemate/lib/swipper/swiper-bundle.min.css',
            'sh_corpomate_theme/static/src/js/index.js',
            'sh_corpomate_theme/static/src/js/wow_min.js',
            "sh_corpomate_theme/static/src/js/render_tess_new.js",
            'sh_corpomate_theme/static/src/js/our_partner_category.js',
            'sh_corpomate_theme/static/src/js/custom.js',
            'sh_corpomate_theme/static/src/js/timer_snippet/s_offer.js',

            # TODO comment this in v18 
            # 'sh_corpomate_theme/static/src/js/vertical_carousel.js',
            'sh_corpomate_theme/static/src/js/s_progress.js',
            'sh_corpomate_theme/static/src/js/s_counter.js',
            'sh_corpomate_theme/static/src/js/extra_addons/onemate/counter.js',
            'sh_corpomate_theme/static/src/js/extra_addons/onemate/swiper_slider_public_widget.js',
            'sh_corpomate_theme/static/src/js/extra_addons/onemate/lib/swipper/swiper-bundle.min.js',
            "sh_corpomate_theme/static/src/js/onepage_2.js",

            # sh_blog _filter_snippet
            "sh_corpomate_theme/static/src/js/extra_addons/sh_blog_filter_snippet/s_post.js",
            "sh_corpomate_theme/static/src/scss/extra_addons/sh_blog_filter_snippet/s_post.scss",

            # sh_cookie_notice
            "sh_corpomate_theme/static/src/css/extra_addons/sh_cookie_notice/cookieconsent.min.css",

            # sh_website_popup
            "sh_corpomate_theme/static/src/scss/extra_addons/sh_website_popup/sh_website_popup.scss",

            # TODO comment this in v18 ( NOTE : no need to change cookie notice working fine s)
            # "sh_corpomate_theme/static/src/js/extra_addons/sh_website_popup/jquery_cookie.js",
            "sh_corpomate_theme/static/src/js/extra_addons/sh_website_popup/sh_website_popup.js",

            # sh_website_portfolio
            "sh_corpomate_theme/static/src/scss/extra_addons/sh_website_portfolio/sh_website_portfolio.scss",
            # TODO comment this in v18 ( CHECKING )
            # "sh_corpomate_theme/static/src/libs/lc_lightbox/lc_lightbox.lite.js",
            "sh_corpomate_theme/static/src/js/extra_addons/portfolio/portfolio.js",


            # sh_notice_board
            "sh_corpomate_theme/static/src/js/extra_addons/sh_notice_board/snippets.js",
            "sh_corpomate_theme/static/src/scss/extra_addons/sh_notice_board/snippets.scss",

            # sh_website_wtsapp
            "sh_corpomate_theme/static/src/css/extra_addons/sh_website_wtsapp/sh_website_wtsapp.css",
            "sh_corpomate_theme/static/src/js/extra_addons/sh_website_wtsapp/detect_mobile.js",

            # sh_website_quote
            "sh_corpomate_theme/static/src/js/extra_addons/sh_website_quote/custom.js",
            "sh_corpomate_theme/static/src/scss/extra_addons/sh_website_quote/website_quote.scss",

            # sh_website_coming_soon
            "sh_corpomate_theme/static/src/css/extra_addons/sh_website_coming_soon/animate.css",
            "sh_corpomate_theme/static/src/css/extra_addons/sh_website_coming_soon/coming_soon.css",
            "sh_corpomate_theme/static/src/js/extra_addons/sh_website_coming_soon/countdown.js",

            

            # sh_image_hotspot_snippet
            "sh_corpomate_theme/static/src/js/extra_addons/sh_image_hotspot_snippet/custom.js",
            "sh_corpomate_theme/static/src/js/extra_addons/sh_image_hotspot_snippet/frontend.js",
            "sh_corpomate_theme/static/src/scss/extra_addons/sh_image_hotspot_snippet/style.scss",

            # sh_snippet_adv
            "sh_corpomate_theme/static/src/libs/aos/aos_extra.css",
            "sh_corpomate_theme/static/src/libs/aos/aos.css",
            "sh_corpomate_theme/static/src/libs/aos/aos.js",
            "sh_corpomate_theme/static/src/libs/aos/layout.css",
            #"sh_corpomate_theme/static/src/libs/owl/owl.carousel.js",
            #"sh_corpomate_theme/static/src/libs/owl/owl.carousel.min.css",
            #"sh_corpomate_theme/static/src/libs/owl/owl.theme.default.min.css",
            "sh_corpomate_theme/static/src/libs/owl/owl.carousel.min.js",
            "sh_corpomate_theme/static/src/libs/owl/owl.carousel.min.css",

            # TODO comment this for v18 migration ( LOAD JS IN COOKIE TMPL )
            # "sh_corpomate_theme/static/src/libs/tilt/tilt.jquery.js",

            "sh_corpomate_theme/static/src/js/extra_addons/sh_snippet_adv/s_animation.js",
            "sh_corpomate_theme/static/src/scss/extra_addons/sh_snippet_adv/image_mask.scss",

            # sh_website_preloader,
            "sh_corpomate_theme/static/src/css/extra_addons/sh_website_preloader/preloader.css",
            "sh_corpomate_theme/static/src/js/extra_addons/sh_website_preloader/preloader.js",

            # sh_website_store_locator
            # TODO comment this for v18 migration
            # "sh_corpomate_theme/static/src/js/extra_addons/sh_website_store_locator/bootstrap-multiselect.js",
            "sh_corpomate_theme/static/src/js/extra_addons/sh_website_store_locator/custom.js",
            "sh_corpomate_theme/static/src/scss/extra_addons/sh_website_store_locator/style.scss",
            "sh_corpomate_theme/static/src/xml/store_in_details.xml",

            "sh_corpomate_theme/static/src/js/theme_scroll_animation.js",

            ## sh_website_megamenu
            # "sh_corpomate_theme/static/src/scss/extra_addons/mega_menu/sh_website_megamenu.scss",
            # "sh_corpomate_theme/static/src/js/extra_addons/sh_website_megamenu/sh_updated.js",
            # "sh_corpomate_theme/static/src/js/extra_addons/sh_website_megamenu/sh_megamenu.js",
            # TODO comment this for v18 migration

            # "sh_corpomate_theme/static/src/js/extra_addons/onemate/lib/aos/aos.js",
           

        ],

        'web.assets_backend': [
            # sh_web_push_notifications
            "https://www.gstatic.com/firebasejs/8.4.3/firebase-app.js",
            "https://www.gstatic.com/firebasejs/8.4.3/firebase-messaging.js",
            "sh_corpomate_theme/static/src/js/extra_addons/sh_web_push_notifications/firebase.js",
            
            "sh_corpomate_theme/static/src/xml/google_place_widget.xml",
            "sh_corpomate_theme/static/src/scss/extra_addons/sh_website_store_locator/style_backend.scss",
            "sh_corpomate_theme/static/src/js/extra_addons/sh_website_store_locator/store_locator_autocomplete.js",
            
            
            "sh_corpomate_theme/static/src/icon_picker_popover/icon_picker_popover.js",
            "sh_corpomate_theme/static/src/icon_picker_popover/icon_picker_popover.xml",
            "sh_corpomate_theme/static/src/icon_picker_char_field/icon_picker_char_field.js",
            "sh_corpomate_theme/static/src/icon_picker_char_field/icon_picker_char_field.xml",
            "sh_corpomate_theme/static/src/icon_picker_popover/icon_picker_popover.scss",

        ],
        "sh_corpomate_theme.assets_icon":{
            "sh_corpomate_theme/static/src/icon_picker_popover/icon_picker_popover_data.js",
        },
        'web._assets_primary_variables': [
            'sh_corpomate_theme/static/src/scss/theme/font/font_palettes.scss',
            'sh_corpomate_theme/static/src/scss/theme/primary_variables.scss',

        ],

        'website.assets_wysiwyg': [
            'sh_corpomate_theme/static/src/xml/html_snippet_popup.xml',
            'sh_corpomate_theme/static/src/js/extra_addons/sh_html_snippet/sh_html_snippet.js',
            'sh_corpomate_theme/static/src/xml/offer_timer_popup.xml',
            # TODO add this file in frontend 
            # 'sh_corpomate_theme/static/src/xml/website.editor.xml',
            'sh_corpomate_theme/static/src/xml/offer_timer_popup.xml',

            # sh_snippet_builder
            "sh_corpomate_theme/static/src/js/extra_addons/sh_snippet_builder/website.editor.js",
            "sh_corpomate_theme/static/src/xml/sh_snippet_builder_popup.xml",

            # sh_image_hotspot_snippet
            "sh_corpomate_theme/static/src/js/extra_addons/sh_image_hotspot_snippet/image_hotspot.js",

            # sh_snippet_Adv
            "sh_corpomate_theme/static/src/scss/extra_addons/sh_snippet_adv/snippets_options.scss",
            "sh_corpomate_theme/static/src/js/extra_addons/sh_snippet_adv/svg_editor.js",    
            # TODO comment this for v18 migration       
            # "sh_corpomate_theme/static/src/lib/tilt.js",            

            # sh_website_megamenu
            'sh_corpomate_theme/static/src/js/extra_addons/sh_website_megamenu/snippets.options.js',
        ],
		'web_editor.assets_wysiwyg': [
            # 'sh_corpomate_theme/static/src/js/OdooEditor.js',
            
        ],

    },

    "images": [
        "static/description/splash-screen.png",
        "static/description/splash-screen_screenshot.gif",
    ],
    "live_test_url": "https://softhealer.com/support?ticket_type=demo_request",
    "qweb": ["static/src/xml/website.editor.xml"],
    "auto_install": False,
    "installable": True,
    "price": 120,
    "currency": "EUR"
}
