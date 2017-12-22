$(function() {


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});

$('button#btn-confirm-upload').click(function(event){

    var orders = [];
    $("tr.table-row").each(function(){
        var order = {}
        order['building'] = $(this).find('p[name*="building"]').text();
        order['ws_name'] = $(this).find('p[name*="ws_name"]').text();
        order['location'] = $(this).find('p[name*="location"]').text();
        order['floor'] = $(this).find('p[name*="floor"]').text();
        order['ws_phone'] = $(this).find('p[name*="ws_phone"]').text();
        order['product_name'] = $(this).find('p[name*="product_name"]').text();
        order['sizencolor'] = $(this).find('p[name*="sizencolor"]').text();
        order['price'] = $(this).find('p[name*="price"]').text();
        order['count'] = $(this).find('p[name*="count"]').text();

        orders.push(order)


    });
    
    $.ajax({
        url : "upload_bulk/",
        type : "POST",
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(orders),
        dataType: 'text',
        success : function(result){

            window.location.href = "order_list/"

        }


    });
});

$('form#excel-modal').on('submit', function(event){
    event.preventDefault();
    var formData = new FormData(this);


    console.log("form submitted!")  // sanity check
    create_post(formData);

});

function create_post(formData) {
    console.log("create post is working!"); // sanity check
    $.ajax({
        url : "modal_view/",
        type : "POST",
        data : formData,
        processData : false,
        contentType: false,
        success : function(response, data){


            $('#excel_modal').find('.modal-body').html(response);
            $('#excel_modal').modal('show');



        }


    });


};