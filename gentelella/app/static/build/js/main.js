// document.getElementById("check-username").addEventListener("click", duplicate_user);
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

jQuery(window).load(function () {
    //alert('page is loaded');

    $('.flat').each(function(i, obj){
        //$(this).css
    });

});

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$('button#btn-confirm-upload').click(function(event){

    var data= {};
    var retailer_name = "";
    retailer_name = $('h3[name=retailer_name]').text();
    data.retailer_name = retailer_name;

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

    data.orders = orders

    $.ajax({
        url : "/upload_bulk/",
        type : "POST",
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify([data]),
        dataType: 'text',
        success : function(result){
            window.location.href = "/order_list/";
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
        url : "/modal_view/",
        type : "POST",
        data : formData,
        processData : false,
        contentType: false,
        success : function(response, data){

            $('#excel_modal').find('.modal-body').html(response);
            $('#excel_modal').modal('show');

        },

    });
};

