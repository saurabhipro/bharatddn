$(document).ready(function() {
    $("#sh_wq_website_quote_form").submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: '/sh_website_quote/contact_us',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({'jsonrpc': "2.0", 'method': "call", "params": {
                contact_name: $('input[name="contact_name"]').val(),
                phone: $('input[name="phone"]').val(),
                email_from: $('input[name="email_from"]').val(),
                partner_name: $('input[name="partner_name"]').val(),
                name: $('input[name="name"]').val(),
                description: $('textarea[name="description"]').val()}}),
            success: function(data) {
                if (data.result.error) {
                    $("#sh_wq_website_quote_thankyou_msg").show();
                    $("#sh_wq_website_quote_thankyou_msg").html('<div class="alert alert-danger" style="margin-bottom:0px;"><strong>Failure to request a quote.</strong></div>');
                    return;
                }
                else{
                    $("#sh_wq_website_quote_form").hide();
                    $("#sh_wq_website_quote_thankyou_msg").show();
                    $("#sh_wq_website_quote_thankyou_msg").html('<div class="alert alert-success" style="margin-bottom:0px;"><strong>Your message has been sent successfully. We will get back to you shortly.</strong></div>');
                }
            },
        });
        return false;
    });

    // Empty form each time when show modal
    $("#sh_wq_website_quote_model").on("show.bs.modal", function() {
        $("#sh_wq_website_quote_form").show();
        $("#sh_wq_website_quote_thankyou_msg").hide();
        $("#sh_wq_website_quote_form")[0].reset();
    });
});

//});
