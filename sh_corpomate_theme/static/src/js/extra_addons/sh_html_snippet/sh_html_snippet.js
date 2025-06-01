/** @odoo-module **/

import options from "@web_editor/js/editor/snippets.options";
import { renderToElement } from "@web/core/utils/render";


    
    // ajax.loadXML("/sh_html_snippet/static/src/xml/html_snippet_popup.xml", core.qweb);

    // SNIPPET OPTION.
    options.registry.js_editor_sh_html_snippet = options.Class.extend({
        start: function () {
            var self = this;
            var def = this._super.apply(this, arguments);
            return def;
        },

        sh_html_snippet_configure: function (previewMode, value) {
            var self = this;
			
            if (previewMode === false || previewMode === "click") {
                // MAKE MODEL
                self.$modal = $(renderToElement("sh_corpomate_theme.sh_popup_html_snippet"));
                // REMOVE PREVIOUS APPENDED MODEL
                $("body > #js_id_model_html_snippet_config").remove();

                // ADD MODEL TO BODY IN ORDER TO OPEN IT.
                self.$modal.appendTo("body");
				self.$modal.modal('show');
                // CLICK ON SAVE CHANGES BUTTON ADD CODE TO PAGE.
                self.$modal.on("click", ".js_cls_btn_apply_html_snippet_config", function () {
                    // JS
                    var js = "<script type='text/javascript'>" + self.$modal.find("#js_id_sh_html_snippet_js_code").val() + "</script>";

                    //                	var js = "<script type='text/javascript'>" +
                    //                			"odoo.define(function (require) {" +
                    //                			self.$modal.find('#js_id_sh_html_snippet_js_code').val() +
                    //                			"});" +
                    //                			"</script>" ;

                    // STYLE
                    var style = "<style>" + self.$modal.find("#js_id_sh_html_snippet_css_code").val() + "</style>";

                    // HTML
                    var html = self.$modal.find("#js_id_sh_html_snippet_html_code").val();

                    // PUT/ADD CODE IN ODOO PAGE.
                    self.$target.empty().append(js + style + html);

                    // CLOSE THE MODEL
                    self.$modal.find(".js_cls_btn_close_html_snippet_config").click();
					self.$modal.modal('hide');
                });

                self.$modal.on("click", ".js_cls_btn_close_html_snippet_config", function () {
                    $('#js_id_model_html_snippet_config').css("display","");
                });


                // REMOVE MODEL
                self.$modal.modal();
            }
            return self;
        },

        onBuilt: function () {
            var self = this;
            this._super();
            this.sh_html_snippet_configure("click");
        },
    });
