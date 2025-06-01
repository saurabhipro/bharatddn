$(document).ready(function() {
    var date = new Date();
    var limitDays = $("#days").val();
    var sh_cookie_key = window.location.hostname + "shWebsitePopupEndDate";
    date.setTime(date.getTime() + limitDays * 24 * 60 * 60 * 1000); // Add days to current time
    let expires = "expires=" + date.toUTCString();
    let cookies = document.cookie.split("; ");
    var setCookie = false;
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].split("=");
        if (cookie[0] === sh_cookie_key) {
            setCookie = cookie[1]; 
        }
    }
    if (setCookie === false) {
        $("#sh_swp_model_popup").modal("show");
    } else {
        $("#sh_swp_model_popup").modal("hide");
    }
    $(".submit_btn").click(function() {
        document.cookie = sh_cookie_key + "=Model_shown; " + expires + "; path=/";
    });


    // Define cookie name based on hostname
    var corpomateDarkMode = window.location.hostname + "corpomateDarkMode";

    // Dark mode icons
    var dark_mode_on_cnt = "<div class='dark_mode_inner dark_off_mode_inter_wrapper js_cls_dark_mode' title='Disable Dark Mode'>" +
        "<i class='fa fa-sun-o'></i>" +
        "</div>";

    var dark_mode_off_cnt = "<div class='dark_mode_inner dark_on_mode_inter_wrapper js_cls_dark_mode' title='Enable Dark Mode'>" +
        "<i class='fa fa-moon-o'></i>" +
        "</div>";

    // Get cookies and check if dark mode cookie is set
    var setCookieDarkMode = false;

    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].split("=");
        if (cookie[0] === corpomateDarkMode) {
            setCookieDarkMode = cookie[1];
        }
    }

    // If cookie is not set, set it to default (light mode)
    if (!setCookieDarkMode) {
        document.cookie = corpomateDarkMode + "=dark_mode_is_off; path=/";
        setCookieDarkMode = "dark_mode_is_off"; // Immediately apply default
    }

//    console.log("\n\n setCookieDarkMode", setCookieDarkMode);

    if (setCookieDarkMode === "dark_mode_is_on") {
        $('#wrapwrap').addClass('dark_mode_is_on').removeClass('dark_mode_is_off');
        $('#wrapwrap').find('.dark_mode_inner').replaceWith(dark_mode_on_cnt);
    } else if (setCookieDarkMode === "dark_mode_is_off") {
        $('#wrapwrap').addClass('dark_mode_is_off').removeClass('dark_mode_is_on');
        $('#wrapwrap').find('.dark_mode_inner').replaceWith(dark_mode_off_cnt);
    }
    
    // var get_mode = $.cookie("corpomateDarkMode") || false;

    // if(!get_mode){
    //     $.cookie('corpomateDarkMode', 'dark_mode_is_off', { expires: null });
    // }
    // var get_mode = $.cookie("corpomateDarkMode") || false;
    
    // if (get_mode && get_mode == "dark_mode_is_on"){
    //     $('#wrapwrap').addClass('dark_mode_is_on')
    //     $('#wrapwrap').removeClass('dark_mode_is_off')
    //     $('#wrapwrap').find('.dark_mode_inner').replaceWith(dark_mode_on_cnt)
    // }
    // if(get_mode && get_mode == "dark_mode_is_off"){
    //     $('#wrapwrap').addClass('dark_mode_is_off')
    //     $('#wrapwrap').removeClass('dark_mode_is_on')
    //     $('#wrapwrap').find('.dark_mode_inner').replaceWith(dark_mode_off_cnt)
    // }
});