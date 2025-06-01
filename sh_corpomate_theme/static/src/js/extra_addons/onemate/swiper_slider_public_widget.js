/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

    // require('web.dom_ready');

publicWidget.registry.InitializeSlider = publicWidget.Widget.extend({
    selector: ".js_cls_swiper_slider_wrapper",
    events: {
        "click .js_cls_simulating_user_interaction_btn": "_on_click_js_cls_simulating_user_interaction_btn",
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * We don't want to do anything when user interaction btn clicked
     * just click button when widget start in order to prevent video playing error in chrome
     * https://developer.chrome.com/blog/autoplay/
     *
     * @override
     * @param {Event} ev
     */
    _on_click_js_cls_simulating_user_interaction_btn: function (ev) {
        ev.stopPropagation();
        ev.preventDefault();
    },

    // --------------------------------------------------------------
    // INITIALIZE SLIDER LIBRARY
    // --------------------------------------------------------------

    // var swiper = new Swiper(".mySwiper",

    //     {
    //         effect: "coverflow",
    //         grabCursor: true,
    //         centeredSlides: true,
    //         slidesPerView: "auto",
    //         coverflowEffect: {
    //             rotate: 50,
    //             stretch: 0,
    //             depth: 100,
    //             modifier: 1,
    //             slideShadows: true,
    //         },
    //         pagination: {
    //             el: ".swiper-pagination",
    //         },
    //     }

    // );

    willStart: function () {
        var self = this;
        res = this._super.apply(this, arguments);
        // IN ORDER TO TRIGGER USER INTERSACTION
        self.$(".js_cls_simulating_user_interaction_btn").click();
        self.$(".js_cls_simulating_user_interaction_btn").trigger("click");
        return res;
    },

    /**
     * @override
     */
    init: function (parent, params) {
        this._super.apply(this, arguments);
        this.timer = 0;
        this.video_length = 9;
    },

    /**
     *
     */
    _update_timer: function () {
        if (this.timer == this.video_length) {
            this.timer = 0;
            if ( this.swiper_video ){
                this.swiper_video.slideNext();
            }

        }
        this.timer += 1;
    },

    start: function () {
        var self = this;
        this.video_timer_interval = null;
        self._update_timer();
        self.video_timer_interval = setInterval(self._update_timer.bind(self), 1000);
        self.swiper_video = new Swiper(".js_cls_video_swiper_container", {
            loop: true,
            // speed: 1000,
            // autoplay: {
            //    delay: 3000,
            // },
            effect: "coverflow",
            grabCursor: true,
            centeredSlides: true,
            slidesPerView: "auto",
            coverflowEffect: {
                rotate: 0,
                stretch: 80,
                depth: 200,
                modifier: 1,
                slideShadows: false,
            },
            pagination: {
                el: ".js_cls_swiper_pagination",
            },
            on: {
                update: function () {
                    self.timer = 0;
                },
                observerUpdate: function () {
                    self.timer = 0;
                },
                beforeInit: function () {
                },
                afterInit: function () {
                    // this.visibleSlidesIndexes
                    self.timer = 0;
                    $(this.visibleSlides[0]).find("video").get(0).pause();
                    $(this.visibleSlides[0]).find("video").get(0).currentTime = 0;


                    $(this.visibleSlides[1]).find("video").get(0).currentTime = 0;
                    $(this.visibleSlides[1]).find("video").get(0).play();


                    $(this.visibleSlides[2]).find("video").get(0).pause();
                    $(this.visibleSlides[2]).find("video").get(0).currentTime = 0;

                    var dont_pause_this_slide = this.visibleSlidesIndexes[1];

                    // PAUSE ALL VIDEO WHEN SLIDER INIT.
                    _.each(this.slides, function (slide_el, v) {
                        var $slide_el = $(slide_el);
                        if (v == dont_pause_this_slide) {
                            self.video_length = $slide_el.find("video").data("video_length") || 9;
                            return;
                        }

                        try {
                            // option 1
                            $slide_el.find("video").get(0).pause();
                            // option 2
                            if (self.play_promise !== undefined) {
                                self.play_promise
                                    .then((_) => {
                                        // Automatic playback started!
                                        // Show playing UI.
                                        // We can now safely pause video...
                                        $slide_el.find("video").get(0).pause();
                                        // $slide_el.find("video").get(0).currentTime = 0;
                                        //$slide_el.find('video').trigger('pause');
                                    })
                                    .catch((error) => {
                                        // Auto-play was prevented
                                        // Show paused UI.
                                    });
                            }
                        } catch (exceptionVar) { }
                    });


                },
                activeIndexChange: function (ev) {
                    _.each(this.slides, function (slide_el, v) {
                        var $slide_el = $(slide_el);
                        if (v == ev.activeIndex) {
                            try {
                                // $slide_el.find('video').trigger('play');
                                $slide_el.find("video").get(0).currentTime = 0;
                                self.play_promise = $slide_el.find("video").get(0).play();
                                // HERE 9 IS A MAXIMUM VIDEO LENGTH FROM ALL VIDEOS.
                                self.video_length = $slide_el.find("video").data("video_length") || 9;
                            } catch (exceptionVar) { }
                        } else {
                            try {
                                // option 1
                                $slide_el.find("video").get(0).pause();
                                // $slide_el.find("video").get(0).currentTime = 0;
                                //$slide_el.find('video').trigger('pause');

                                // option 2
                                if (self.play_promise !== undefined) {
                                    self.play_promise
                                        .then((_) => {
                                            // Automatic playback started!
                                            // Show playing UI.
                                            // We can now safely pause video...
                                            $slide_el.find("video").get(0).pause();
                                            // $slide_el.find("video").get(0).currentTime = 0;
                                            //$slide_el.find('video').trigger('pause');
                                        })
                                        .catch((error) => {
                                            // Auto-play was prevented
                                            // Show paused UI.
                                        });
                                }
                            } catch (exceptionVar) { }
                        }
                    });
                },
            },
        });

        return this._super.apply(this, arguments);
    },

    // publicWidget.registry.ActiveSliderVideo = publicWidget.Widget.extend({
    //     selector: ".swiper-slide-active",

    //     // --------------------------------------------------------------
    //     // PLAY VIDEO FOR ACTIVE SLIDER
    //     // --------------------------------------------------------------

    //     /**
    //      * @override
    //      */
    //     start: function () {
    //         var def = this._super.apply(this, arguments);
    //         return def;
    //     },
    // });

    // --------------------------------------------------------------
    // PLAY VIDEO FOR ACTIVE SLIDER
    // --------------------------------------------------------------
});
