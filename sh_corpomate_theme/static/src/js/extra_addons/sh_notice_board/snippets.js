/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { KeepLast } from "@web/core/utils/concurrency";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.sh_nb_notice_board_horizontal_tmpl_1 = publicWidget.Widget.extend({
    selector: ".sh_nb_notice_board_main_horizontal_marquee_cls_1 , .sh_nb_notice_board_main_vertical_marquee_cls_1, .js_cls_sh_nb_notice_board_vertical_tmpl_4_render_dynamic_area",
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
        var self = this;
        var tempalte = this.$el.attr("data-item_template") || false;
        var section_classes = false;
        var rows = false;
        if (this.$el.parents("section").attr("class")) {
            section_classes = this.$el.parents("section").attr("class");
        }

        if (section_classes) {
            var pos = section_classes.search("newscount_");
            if (pos != -1) {
                var newscount_cls = section_classes.substring(pos, pos + 12);
                var rows = newscount_cls.replace("newscount_", "");
            }
        }
        this.$el.find("span").remove();
        this.$el.find("div").remove();

        if (self.$el.hasClass('js_cls_sh_nb_notice_board_vertical_tmpl_4_render_dynamic_area')) {
            self.$el.empty();
        }
        rpc("/get_latest_news", {
            "limit": rows,
        }).then((data) => {
            jQuery.each(data, function (key, value) {

                if (self.$el.hasClass('js_cls_sh_nb_notice_board_vertical_tmpl_4_render_dynamic_area')) {
                    self.$el.append("<li><a href='#'>" + value.desc + "</a></li>");
                }
                else if (self.$el.parents('div').attr('class') == 'sh_vertical_main row') {
                    self.$el.append("<div class='sh_news'><h4>" + value.name + "</h4><p>" + value.desc + "</p></div>");
                }
                else if (self.$el.parents('div').attr('class') == 'sh_vertical_div_js_cls container-fluid row') {
                    self.$el.append("<div class='sh_news_box'><h4>" + value.name + "</h4><p>" + value.desc + "</p></div>");
                }
                else {
                    self.$el.append("<span>" + value.desc + "</span>");
                }
            });
        });

        return this._super.apply(this, arguments);

    },
});
