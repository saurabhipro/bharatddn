$(document).ready(function(){
	$('[data-bs-toggle="popover"]').popover()
	
	$('body').click(function (e) {
	    $('[data-bs-toggle=popover]').each(function () {
			// hide any open popovers when the anywhere else in the body is clicked
	        if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
	            $(this).popover('hide');
	        }
	    });
	});
	
});