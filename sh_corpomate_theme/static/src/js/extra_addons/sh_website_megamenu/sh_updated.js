// A $( document ).ready() block.
$(document).ready(function () {
    /*
     * ==================================================
     * js_cls_sh_megamenu_section_1
     * Show/hide block Accordion
     * ==================================================
     */

    $(".js_cls_sh_megamenu_section_1").on("click", ".sub-heading", function (e) {
        e.preventDefault();
        e.stopPropagation();

        var ul = $(this).closest(".js_cls_mm").find("ul");
        if (ul.is(":visible")) {
            ul.hide();
        } else {
            ul.show();
        }
    });

    /*
     * ==================================================
     * js_cls_sh_megamenu_section_2
     * Show/hide block Accordion
     * ==================================================
     */

    $(".js_cls_sh_megamenu_section_2").on("click", ".sub-heading", function (e) {
        e.preventDefault();
        e.stopPropagation();

        var ele = $(this).closest(".js_cls_mm").find(".sh_acoordion_part");
        if (ele.is(":visible")) {
            ele.hide();
        } else {
            ele.show();
        }
    });

    /*
     * ==================================================
     * js_cls_sh_megamenu_section_4
     * Show/hide block Accordion
     * ==================================================
     */

    // $(".js_cls_sh_megamenu_section_4").on("click", ".sub-heading", function (e) {
    //     e.preventDefault();
    //     e.stopPropagation();

    //     var ele = $(this).closest(".js_cls_accordion_parent").find(".sh_acoordion_part");
    //     if (ele.is(":visible")) {
    //         ele.hide();
    //     } else {
    //         ele.show();
    //     }
    // });

    /*
     * ==================================================
     * js_cls_sh_megamenu_section_15
     * Show/hide block Accordion
     * ==================================================
     */

    // $(".js_cls_sh_megamenu_section_15").on("click", ".js_cls_mm_h4_15", function (e) {
    //     e.preventDefault();
    //     e.stopPropagation();

    //     var ele = $(this).closest(".sh_content").find("ul");
    //     if (ele.is(":visible")) {
    //         ele.hide();
    //     } else {
    //         ele.show();
    //     }
    // });
});