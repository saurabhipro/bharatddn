/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
// import { loadJS } from "@web/core/assets";
import { AssetsLoadingError, loadCSS, loadJS } from '@web/core/assets';
import { _t } from "@web/core/l10n/translation";
// import Dialog from "@web/legacy/js/core/dialog";
import { Dialog } from "@web/core/dialog/dialog";

import { renderToElement } from "@web/core/utils/render";




publicWidget.registry.CustomJsGoogleMap = publicWidget.Widget.extend({
    selector: '.js_cls_store_locator_wrapper',

    events: {
        'click input[name="view-btn-radio"]': '_view_enable',
        'click .store-header .search-store': '_onSearchStore',
        'keypress .store-header #search-input': '_onSearchInput',
        'click .js_cls_current_location': '_onClickCurrentLocation',
        'change #sh_filter_city.filter_store, #sh_filter_state.filter_store, #sh_filter_country.filter_store': '_onChangeFilterCities',
        'click .js_cls_store_direct_link_to_map': '_onClickGoogleDirectLink',
        'click .js_cls_store_more_info': '_onClickStoreMoreInfo',
    },

    _initialise_variable: function () {
        var self = this;
        self.filter_city = [];
        self.filter_state = [];
        self.filter_country = [];
        self.markers = [];
        self.infowindows = [];
        self.openinfo = null;
        self.mapProp;
        self.map;
        self.vals = {};
        self.carrier_value;
        self.show_locator;
        self.initialize_data;
        self.load_count = 0;
        self.shop_count = 0;
        self.bounds;
        self.search_radius = 0;
    },


    /**
         * @constructor
         */
    init: function () {
        var self = this;

        $('input[name="view-btn-radio"]#gridView').click()
        this._view_enable()
        self._initialise_variable();
        self.sh_locator_call_json(self.vals, true);
        this._super.apply(this, arguments);
    },

    start: function () {
        var self = this;

        try {
            const loadBoot = Promise.all([
                // loadJS('https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.js'),
                loadJS('https://github.com/davidstutz/bootstrap-multiselect/blob/master/dist/js/bootstrap-multiselect.js'),
                // loadCSS('https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css'),
                loadCSS('https://github.com/davidstutz/bootstrap-multiselect/blob/master/dist/css/bootstrap-multiselect.css'),
            ])
            console.log('log ==>> LOAD JS MULTISELECT',loadBoot);
        } catch (error) {
            console.log('log ==>> LOAD JS error',error);
            if (!(error instanceof AssetsLoadingError)) {
                throw error;
            }
        }
        setTimeout(function () {
            console.log('log ==>> multiselectInit',$("#sh_filter_city"));
            $("#sh_filter_city").multiselect({
                enableCaseInsensitiveFiltering: true,
                selectedClass: 'active',
            });
            $('#multiple-checkboxes').multiselect({
                includeSelectAllOption: true,
              });
        }, 4000);

        // TODO migration 18 need to check
        // Filter Cities
        

        // Filter States
        // $("#sh_filter_state").multiselect({
        //     enableCaseInsensitiveFiltering: true,
        //     selectedClass: 'active',
        // });

        // Filter Countries
        // $("#sh_filter_country").multiselect({
        //     enableCaseInsensitiveFiltering: true,
        //     selectedClass: 'active',
        // });

    },

    _onSearchStore: function (ev) {
        var self = this;
        self.search_by_address_init();
    },

    _onSearchInput: function (ev) {
        var self = this;
        if (ev.which == 13) {
            self.search_by_address_init();
        }
    },

    search_by_address_init: function () {
        var self = this;
        var search_string = ($('#search-input').val()).toLowerCase();
        $('.store-not-found').hide();
        $('.extra-information').hide();
        self.hide_info_window();
        self.search_by_address(search_string);
    },

    hide_info_window: function () {
        var self = this;
        if (self.openinfo != null) {
            self.infowindows[self.openinfo].close(self.map, self.markers[self.openinfo]);
            $('#' + (self.openinfo + 1) + '').find('.store-list').removeClass('selected');
            self.openinfo = null;
        }
    },

    show_all_shop_list: function () {
        var self = this;
        $('.store-menu sh_store_section.gridView').removeClass('shop-hidden');
        $(".store-lable").text("" + Object.keys(self.initialize_data.map_stores_data).length + _t(" Store(s)"));
        this.shop_count = ((Object.keys(self.initialize_data.map_stores_data).length) - 1);
    },

    search_by_address: function (search_string) {
        var self = this;
        var main_addr = '';
        var count = 0;
        var not_have_cat = 0;
        self.bounds = new google.maps.LatLngBounds();

        $.each(self.initialize_data.map_stores_data, function (key, value) {
            main_addr = self.get_search_main_address(value);

            if (!main_addr) {
                main_addr = ''
            }
            var match = main_addr.indexOf(search_string);
            if (match >= 0) {
                self.show_marker_and_shop(parseInt(key));
                count++;
            } else {

                self.hide_marker_and_shop(parseInt(key));
            }
        });
        if (count >= 1) {
            self.map.fitBounds(self.bounds);
        }
        else {
            self.get_shop_nearest_address(search_string);
        }
        $(".store-lable").text("" + count + _t(" Store(s)"));
    },

    get_shop_nearest_address: function (search_string) {
        var self = this;
        var latitude = 0;
        var longitude = 0;
        var geocoder = new google.maps.Geocoder();
        var count = 0;
        $('.store_locator_loder').show();
        self.bounds = new google.maps.LatLngBounds();
        geocoder.geocode({
            'address': search_string
        }, function (results, status) {
            $('.store_locator_loder').hide();
            if (status == google.maps.GeocoderStatus.OK) {
                latitude = results[0].geometry.location.lat();
                longitude = results[0].geometry.location.lng();
                $.each(self.initialize_data.map_stores_data, function (key, value) {
                    var d = self.distance_between_points(latitude, longitude, value.store_lat, value.store_lng);
                    if (d <= self.search_radius) {
                        self.show_marker_and_shop(parseInt(key));
                        count++;
                    } else {
                        self.hide_marker_and_shop(parseInt(key));
                    }
                });
                if (count == 0) {
                    $('.store-not-found').show();
                } else {
                    self.map.fitBounds(self.bounds);
                    $('.extra-information.alert-info').html("Result not found for zip <b><i style='color: #ff0000;'>" + search_string + "</i></b>, showing results for nearest shop form your serach.");
                    $('.extra-information').show();
                }
                $(".store-lable").text("" + count + _t(" Store(s)"));
            } else {
                $('.store-not-found').show();
            }
        });
    },

    get_search_main_address: function (store) {
        var self = this;
        var main_addr = store.store_name.toLowerCase();
        if (store.store_address[0])
            main_addr += store.store_address[0].toLowerCase() + ' ';
        if (store.store_address[1])
            main_addr += store.store_address[1].toLowerCase() + ' ';
        if (store.store_address[2])
            main_addr += store.store_address[2].toLowerCase() + ' ';
        if (store.store_address[3])
            main_addr += store.store_address[3].toLowerCase() + ' ';
        if (store.store_address[4])
            main_addr += store.store_address[4].toLowerCase() + ' ';
        return main_addr
    },

    /**
     * @private
     * @param {Event} ev
     */
    _onClickCurrentLocation: function (ev) {
        var self = this;
        this.getLocation(self.initialize_data.map_stores_data);
    },

    /**
     * @private
     */
    getLocation: function (stores) {
        var self = this;
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(async function (position) {
                var current_latitude = position.coords.latitude
                var current_longitude = position.coords.longitude;

                var dist_dic = await rpc('/store/sh_store_locator/current_location', {
                    current_latitude: current_latitude,
                    current_longitude: current_longitude,
                })
                if (dist_dic) {
                    $.each(stores, function (key, value) {
                        if (value.store_name == dist_dic.store_name) {
                            self.show_marker_and_shop(parseInt(key))
                        }
                        else {
                            self.hide_marker_and_shop(parseInt(key))
                        }
                    });
                }



            });
        } else {
            alert("Browser doesn't support geolocation!");
        }
    },

    /**
     * @private
     */
    errorCallback: function (error) {
        console.log(error.code + ":" + error.message);
    },

    _onClickGoogleDirectLink: function (ev) {
        ev.stopPropagation();
        ev.preventDefault();
        var $button = $(ev.currentTarget)
        var store_name = $button.parents('.main_store_info').find('.js_cls_store_name').text()
        store_name = encodeURIComponent(store_name);
        var gmap = 'https://www.google.com/maps/search/?api=1&query='
        var GmapUrl = gmap + store_name

        window.open(GmapUrl, '_blank');
    },

    _onClickStoreMoreInfo: function (ev) {
        ev.stopPropagation();
        ev.preventDefault();
        var $button = $(ev.currentTarget)
        var StoreId = $button.parents('.store_box').find('input[name="store-id"]').val()

        if (StoreId) {
            rpc("/sh_get_store_details_template", {
                "StoreId": StoreId,
            }).then((data) => {
                var stores = data['stores'];
                if (data && data.stores) {
                    const dialog = new Dialog(this, {
                        size: "medium",
                        title: _t("Store Details"),
                        $content: renderToElement('sh_corpomate_theme.StoreMoreDetails', {
                            stores: stores,
                        }),
                        buttons: [
                            { text: _t("Close"), close: true },
                        ],
                    }).open();

                    dialog.opened().then(function () {
                        dialog.$footer.removeClass('justify-content-sm-start');
                        dialog.$footer.removeClass('justify-content-around');
                    });

                }
            });
        }
    },




    // _onSearchFilterStore: function(ev) {
    //     var self = this;
    //     self.filter_city = []
    //     $('input[name="filter_city"]:checked').each(function(i, values){
    //         var city_name = $(values).parents('.form-check').find('label').text();
    //         self.filter_city.push(city_name)
    //     });

    //     self.filter_state = []
    //     $('input[name="filter_state"]:checked').each(function(i, values){
    //         var state_name = $(values).parents('.form-check').find('label').text();
    //         self.filter_state.push(state_name)
    //     });

    //     self.filter_country = []
    //     $('input[name="filter_country"]:checked').each(function(i, values){
    //         var country_name = $(values).parents('.form-check').find('label').text();
    //         self.filter_country.push(country_name)
    //     });

    //     $.each(self.initialize_data.map_stores_data, function(key, value) {
    //         if ( $.inArray(value.store_city, self.filter_city) > -1 || $.inArray(value.store_state, self.filter_state) > -1 || $.inArray(value.store_country, self.filter_country) > -1) {
    //             self.show_marker_and_shop(parseInt(key))
    //         }
    //         else{
    //             self.hide_marker_and_shop(parseInt(key))
    //         }
    //         if (self.filter_city == 0 && self.filter_state == 0 && self.filter_country == 0) {
    //             self.show_marker_and_shop(parseInt(key))
    //         }
    //     });


    // },

    show_marker_and_shop: function (key) {
        var self = this;
        if (!self.markers[key].getVisible()) {
            self.markers[key].setVisible(true);
        }
        if (self.bounds !== undefined) {
            self.bounds.extend(self.markers[key].getPosition());
        }

        // $('#' + (key + 1) + '').removeClass('shop-hidden');
        $('[id=' + (key + 1) + ']').removeClass('shop-hidden');
    },

    hide_marker_and_shop: function (key) {
        var self = this;
        if (self.markers[key].getVisible()) {
            self.markers[key].setVisible(false);
        }
        $('[id=' + (key + 1) + ']').addClass('shop-hidden');

    },

    sh_locator_call_json: function (vals, alert_flag) {
        var self = this;
        $('.sh_store_locator_loder').show();

        rpc('/store/sh_store_locator/vals', vals)
            .then(function (data) {
                if (data) {
                    if (self.load_count == 0) {
                        self.initialize_data = data;
                        // self.search_radius = data.map_search_radius;
                    }
                    self.initialize_store_locator(self.initialize_data); //fucntion call
                    //self.load_count++;
                } else if (alert_flag) {
                    alert(_t("No Store Found."));
                }
                $('.sh_store_locator_loder').hide();
            });
    },



    /**
     * @private
     * @param {Event} ev
     */
    _view_enable: function (ev) {
        var self = this
        var $store_grid_view = $(".sh_store_section.gridView");
        var $store_list_view = $(".sh_store_section.listView");
        this.btn_radio = $('input[name="view-btn-radio"]:checked').attr('id');


        if (this.btn_radio == 'listView') {
            $store_grid_view.addClass('d-none')
            $store_list_view.removeClass('d-none')
            // $store_kanban_view.find('.store_box').addClass('col-lg-12').removeClass('col-lg-4')

        }
        else if (this.btn_radio == 'gridView') {
            $store_list_view.addClass('d-none')
            $store_grid_view.removeClass('d-none')

            // $store_kanban_view.find('.store_box').addClass('col-lg-4').removeClass('col-lg-12')
        }
    },


    load_shop_list: function (key, store, info, table_info) {
        var self = this;

        $('.store-menu .sh_store_section.listView table tbody').append("\
        <tr id=" + (key + 1) + " class='main_store_info store_box'>\
        <input type='hidden' name='store-id' value=" + store.store_id + "></input>\
        " + table_info + "<tr/>")


        $('.store-menu .sh_store_section.gridView').append("<div id=" + (key + 1) + " class=' col-xxl-4 col-xl-4 col-lg-4 col-md-6 col-sm-6 store_box'>\
        <div class='store-list h-100'>\
            <span id='map-lat' data-map-lat=" + store.store_lat + "/>\
            <span id='map-lng' data-map-lng=" + store.store_lng + "/>\
            <input type='hidden' name='store-id' value=" + store.store_id + "></input>\
            <div class='row'>\
            <div class='store-info col-xxl-12 col-xl-12 col-lg-12 col-md-12'>" + info + "</div>\
            </div>\
        </div></div>");
        $('div#' + key + '').find('.store-info img').remove();

        $('#' + (key + 1) + '').on('click', function () {
            if (self.openinfo != null) {
                self.infowindows[self.openinfo].close(self.map, self.markers[self.openinfo]);
                $('#' + (self.openinfo + 1) + '').find('.store-list').removeClass('selected');
                self.openinfo = null;
            }
            $('#' + (key + 1) + '').find('.store-list').addClass('selected');
            self.map.setZoom(11);
            self.markers[key].setVisible(true);
            self.map.setCenter(self.markers[key].getPosition());
            self.infowindows[key].open(self.map, self.markers[key]);
            self.openinfo = key;
        });
    },

    on_map_ready: function () {
        console.log('on_map_ready')
    },


    initialize_store_locator: async function (initialize_data) {
        var self = this;
        var URL = "https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=places"

        window.sh_gmap_callback = self.on_map_ready;

        if (initialize_data.google_api_key) {
            var URL = "https://maps.googleapis.com/maps/api/js?v=3&key=" + initialize_data.google_api_key + "&libraries=places&callback=sh_gmap_callback";
            this._google_map_ready = await loadJS(URL);


            self.mapProp = {
                center: new google.maps.LatLng(initialize_data.map_init_data.map_center_lat, initialize_data.map_init_data.map_center_lng),
                zoom: initialize_data.map_init_data.map_zoom,
                mapTypeId: initialize_data.map_init_data.map_type
            };


            self.map = new google.maps.Map(document.getElementById("googleMap"), self.mapProp);
            // self.load_store_filter_data(initialize_data.cities, initialize_data.countries ,initialize_data.states)
            self.draw_marker_and_info_map(self.map, initialize_data.map_stores_data); //function call
            $('.store-menu .sh_store_section.gridView').append("<div class='store-not-found' style='display:none;'>No Result Found.</div>");
        }
        if (!initialize_data.google_api_key) {
            document.getElementById("googleMap").style.display = "none";
            var message = _t('Please Enter Google Api Key.');
            var dialog = new Dialog(this, {
                size: 'medium',
                title: _t('Warning'),
                $content: $('<p>' + message + '</p>')
            });
            dialog.open();
        }
    },

    gmNoop: function () {
        console.log('\n\n Gmap CALLBACK ============')
    },


    _onChangeFilterCities: function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        var self = this;
        console.log(self);
        var $FilterOption = $(ev.currentTarget);
        console.log($FilterOption);
        console.log($FilterOption.val());



        if ($FilterOption.is('#sh_filter_city')) {
            self.filter_city = $FilterOption.val()
        }
        else if ($FilterOption.is('#sh_filter_state')) {
            self.filter_state = $FilterOption.val()

        }
        else if ($FilterOption.is('#sh_filter_country')) {
            self.filter_country = $FilterOption.val()

        }

        $.each(self.initialize_data.map_stores_data, async function (key, value) {

            if ($.inArray(value.store_city, self.filter_city) > -1 || $.inArray(value.store_state, self.filter_state) > -1 || $.inArray(value.store_country, self.filter_country) > -1) {
                self.show_marker_and_shop(parseInt(key))
            }
            else {
                self.hide_marker_and_shop(parseInt(key))
            }
            if (self.filter_city == 0 && self.filter_state == 0 && self.filter_country == 0) {
                self.show_marker_and_shop(parseInt(key))
            }
        });

    },


    draw_marker_and_info_map: function (map, map_stores_data) {
        var self = this;
        $(".store-lable").text("" + Object.keys(self.initialize_data.map_stores_data).length + _t(" Store(s)"));
        this.shop_count = ((Object.keys(self.initialize_data.map_stores_data).length) - 1);
        $.each(map_stores_data, function (key, values) {
            self.markers.push(new google.maps.Marker({
                position: new google.maps.LatLng(values.store_lat, values.store_lng),
                title: values.store_name,
                map: map,
                icon: '/sh_corpomate_theme/static/src/images/extra_addons/sh_website_store_locator/location_marker.png',
                animation: google.maps.Animation.DROP
            }));
            key = parseInt(key);
            var info = self.get_store_info_html(values);
            var table_info = self.get_store_info_html_for_table(values);

            var store_info = self.get_store_info_html_popup(values);

            self.infowindows.push(new google.maps.InfoWindow({
                content: store_info
            }));
            self.load_shop_list(key, values, info, table_info);
            self.markers[key].addListener('click', function () {
                if (self.openinfo != null) {
                    self.infowindows[self.openinfo].close(map, self.markers[self.openinfo]);
                    $('#' + (self.openinfo + 1) + '').find('.store-list').removeClass('selected');
                    self.openinfo = null;
                }
                self.infowindows[key].open(map, self.markers[key]);
                if (!self.markers[key].getVisible()) {
                    self.markers[key].setVisible(true);
                }
                $('#' + (key + 1) + '').find('.store-list').addClass('selected');
                self.openinfo = key;
                var temp = $(".store-menu").offset().top;
                $(".store-menu").animate({
                    scrollTop: 0
                }, 1, function () {
                    $(".store-menu").animate({
                        scrollTop: $('#' + (key + 1) + '').offset().top - temp
                    }, 1);
                });
            });
        });
    },

    get_store_info_html_popup: function (store) {
        var self = this;
        var addr = '<div><div class="style_2_popup_main_info">';
        if (store.store_name) {
            addr += '<div><strong class="d-inline-block js_cls_store_name">' + store.store_name + '</strong> <br/>';
        }

        if (store.store_address[0]) {
            addr += store.store_address[0] + '<br/>';
        }
        if (store.store_address[1]) {
            addr += store.store_address[1] + ', ';
        }
        if (store.store_address[2]) {
            addr += store.store_address[2] + ', ';
        }
        if (store.store_address[3]) {
            addr += store.store_address[3];
        }
        if (store.store_address[4]) {
            addr += ' - ' + store.store_address[4] + '<br/>';
        }
        addr += '</div>'

        if (store.store_image) {
            addr += '<img style="max-height:70px;" src="' + store.store_image + '"/>';
        }
        addr += '</div>'

        addr += '<div class="style_2_popup_other_info"><div>'

        if (store.store_day_start || store.store_day_end) {
            addr += '<div class="icon_1"><span class="sh_text"><i class="fa fa-calendar "></i><span>' + store.store_day_start + '</span><i class="fa fa-long-arrow-right"></i><span>' + store.store_day_end + '</span></span></div>';
        }

        if (store.sh_time_from || store.sh_time_to) {
            addr += '<div class="icon_1"><span class="sh_text"><i class="fa fa-clock-o "></i><span>' + store.sh_time_from + '</span><i class="fa fa-long-arrow-right"></i><span>' + store.sh_time_to + '</span></span></div>';
        }

        addr += '</div>'

        if (store.sh_store_tag_ids) {
            addr += '<div>'
            $.each(store.sh_store_tag_ids, function (i, value) {
                return addr += '<span class="badge bg-primary">' + value + '</span>'
            });
            addr += '</div>'
        }


        addr += '</div>'
        addr += '</div>'

        return addr;
    },

    get_store_info_html_for_table: function (store) {
        var self = this;
        var addr = '';

        if (store.store_name) {
            addr += '<td class="js_cls_store_name">' + store.store_name + '</td>'
        }
        else {
            addr += '<td class="js_cls_store_name"></td>'
        }

        addr += '<td>'
        if (store.store_address[0]) {
            addr += store.store_address[0] + '<br/>';
        }
        if (store.store_address[1]) {
            addr += store.store_address[1] + ', ';
        }
        if (store.store_address[2]) {
            addr += store.store_address[2] + ', ';
        }
        if (store.store_address[3]) {
            addr += store.store_address[3];
        }
        if (store.store_address[4]) {
            addr += ' - ' + store.store_address[4];
        }
        addr += '</td>'

        addr += '<td>'
        if (store.store_address[5] || store.store_address[6]) {
            if (store.store_address[5]) {
                addr += '<a href="tel:' + store.store_address[5] + '">' + store.store_address[5] + '</a>';
            }
            if (store.store_address[6]) {
                addr += ' , <a href="tel:' + store.store_address[6] + '">' + store.store_address[6] + '</a>';
            }
        }
        addr += '</td>'

        addr += '<td>'
        if (store.store_address[9]) {
            addr += '<a target="_blank" href="' + store.store_address[9] + '"> ' + store.store_address[9] + '</a>'
        }
        addr += '</td>'

        addr += '<td> <button class="btn btn-primary js_cls_store_more_info me-1"><i class="fa fa-info "></i></button><button class="btn btn-primary js_cls_store_direct_link_to_map"><i class="fa fa-map-marker "></i></button></td>'
        return addr
    },

    get_store_info_html: function (store) {

        var self = this;

        var addr = '';
        if (store.store_image) {
            addr += '<div class="store-image"><img style="max-height:70px;" src="' + store.store_image + '"/></div>';
        }

        if (store.store_name) {
            addr += '<div class="main_store_info d-flex justify-content-between" style="font-weight:bold; font-size:16px;"><div class="js_cls_store_name">' + store.store_name + '</div><div class="sh_location_details"><button class="btn btn-primary js_cls_store_more_info me-1"><i class="fa fa-info "></i></button><button class="btn btn-primary js_cls_store_direct_link_to_map"><i class="fa fa-map-marker "></i></button></div></div> <div style="font-weight:400;">';
        }
        if (store.store_address[0]) {
            addr += store.store_address[0] + '<br/>';
        }
        if (store.store_address[1]) {
            addr += store.store_address[1] + ', ';
        }
        if (store.store_address[2]) {
            addr += store.store_address[2] + ', ';
        }
        if (store.store_address[3]) {
            addr += store.store_address[3] + '<br/>';
        }
        if (store.store_address[4]) {
            addr += store.store_address[4] + '<br/>';
        }

        if (store.store_address[5] || store.store_address[6]) {
            addr += '<div class="store-contact tel"><a href="tel:'
            if (store.store_address[5]) {
                addr += store.store_address[5];
            }
            addr += '"><span class="fa fa-phone"></span>';
            if (store.store_address[5]) {
                addr += store.store_address[5];
            }
            addr += '<a/>';
            // if (store.store_address[5] && store.store_address[6]) {
            //     addr += ', ';
            // }
            // if (store.store_address[6]) {
            //     addr += '<a href="tel:' + store.store_address[6] + '">'+ store.store_address[6] + '<a/>'
            // }

            addr += '<div/>';
        }
        if (store.store_address[7]) {
            addr += '<div class="store-contact fax"><span class="fa fa-fax"></span>' + store.store_address[7] + '</div>';
        }
        if (store.store_address[8]) {
            addr += '<div class="store-contact email"><a href="mailto:' + store.store_address[8] + '"><span class="fa fa-envelope"></span>' + store.store_address[8] + '</a></div>';
        }
        if (store.store_address[9]) {
            addr += '<div class="web-addr"><a target="_blank" href="' + store.store_address[9] + '"><span class="fa fa-globe"></span>' + store.store_address[9] + '</a></div>';
        }
        addr += '</div>'
        return addr;
    },

});