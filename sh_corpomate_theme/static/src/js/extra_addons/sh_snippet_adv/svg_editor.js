/** @odoo-module **/

import options from "@web_editor/js/editor/snippets.options";
import { _t } from "@web/core/l10n/translation";

options.registry.shSnippetAdvTiltFeature = options.Class.extend({
    events: Object.assign({}, options.Class.prototype.events || {}, {
        'click .tilt_wrapper we-button': '_onClickTiltWrapper',
    }),

    _onClickTiltWrapper: function () {
        if (this.$target.attr('data-tilt-feature')) {
            this.$target.attr('data-tilt', 'data-tilt');
            this.$target.parent().css("overflow", "unset");
        } else {
            this.$target.removeAttr('data-tilt');
            this.$target.parent().css("overflow", "hidden");
        }
    },
});

options.registry.sh_snippet_adv_svg_editor = options.Class.extend({
    /**
     * @override
     */
    init() {
        this._super(...arguments);
    },

    /**
     * Allows selecting a FontAwesome icon with media dialog.
     *
     * @see this.selectClass for parameters
     */
    changeSvg: function (previewMode, widgetValue, params) {
        var self = this;

        if (this.$target && this.$target.find("svg").length) {
            // Create a custom modal dialog structure
            const modal = `
                <div id="customSvgModal" class="modal" style="display: block;">
                    <div class="modal-content">
                        <span class="close">&times;</span>
                        <h2>${_t("Replace SVG")}</h2>
                        <textarea id="svgTextArea" rows="8" cols="70"></textarea>
                        <div class="modal-footer">
                            <button id="replaceSvgBtn" class="btn-primary">${_t("Replace SVG")}</button>
                            <button id="closeModalBtn" class="btn-secondary">${_t("Close")}</button>
                        </div>
                    </div>
                </div>
                <style>
                    .modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); }
                    .modal-content { background-color: #fff; margin: 15% auto; padding: 20px; border: 1px solid #888; width: 50%; }
                    .modal-footer { margin-top: 20px; text-align: right; }
                    .btn-primary { background-color: #007bff; color: white; padding: 10px 20px; }
                    .btn-secondary { background-color: #6c757d; color: white; padding: 10px 20px; }
                    .close { color: #aaa; float: right; font-size: 28px; font-weight: bold; }
                    .close:hover, .close:focus { color: black; text-decoration: none; cursor: pointer; }
                </style>
            `;

            // Append the modal to the body
            $('body').append(modal);

            // Show the modal
            const modalElement = document.getElementById("customSvgModal");
            modalElement.style.display = "block";

            // Close button functionality
            const closeButton = document.querySelector(".close");
            closeButton.onclick = function () {
                modalElement.style.display = "none";
                modalElement.remove();
            };

            // Replace SVG button functionality
            const replaceSvgButton = document.getElementById("replaceSvgBtn");
            replaceSvgButton.onclick = function () {
                const svgCode = document.getElementById("svgTextArea").value.trim();
                if (svgCode.length) {
                    const svgElement = $(svgCode);
                    self.$target.find("svg").replaceWith(svgElement);
                }
                modalElement.style.display = "none";  // Hide modal
                modalElement.remove();  // Remove modal from DOM after closing
            };

            // Close modal on clicking the "Close" button
            const closeModalButton = document.getElementById("closeModalBtn");
            closeModalButton.onclick = function () {
                modalElement.style.display = "none";
                modalElement.remove();
            };
        }
    },
});
