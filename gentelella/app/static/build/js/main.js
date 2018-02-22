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

$('div#duplicate-username').click(function(event){
    console.log("it works!!");

    var data= {};
    var username = "";
    username = $('input[name="username"]').val();
    data.username = username;



    if (username.length >= 4 && isAlphaNumeric(username)){
        sendAjaxForUserDuplicateCheck(data);
    } else{
         console.log("WRONG!!!");
         var p = $('#check-username');
         p.text("잘못된 아이디 입니다. ");
         p.css('color', 'red');
    }

});

$( "#password-check" ).blur(function() {
    var password = $('#password').val();
    var password_check = $('#password-check').val();
    var p = $('#p-password-check');


    if (password === password_check){
        if (password.length < 8){
            p.text("8자리 이상이어야 합니다");
            p.css('color', 'red');
        } else {
            p.text("");
        }
    } else{

        p.text("비밀번호가 일치하지 않습니다");
        p.css('color', 'red');
    }
});



function isAlphaNumeric(str) {
  var code, i, len;


  for (i = 0, len = str.length; i < len; i++) {
    code = str.charCodeAt(i);
    if (i == 0 && code > 47 && code < 58){
        return false;
    }
    if (!(code > 47 && code < 58) && // numeric (0-9)
        !(code > 64 && code < 91) && // upper alpha (A-Z)
        !(code > 96 && code < 123)) { // lower alpha (a-z)
      return false;
    }
  }
  return true;
};

function sendAjaxForUserDuplicateCheck(data) {

    var csrf = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf);
            }
        }
    });

    $.ajax({
        url : "/check_duplicate_username/",
        type : "POST",
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(data),
        dataType: 'json',
        processData : false,
        contentType: false,
        success : function(result){
            console.log(result['msg']);

            exists = result['msg']
            var p = $('#check-username');

            if(exists === 'ok'){
                p.text("사용가능한 아이디입니다.");
                p.css('color', 'green');
            } else{
                p.text("사용할 수 없는 아이디입니다.");
                p.css('color', 'red');
            }

        },
        error : function(result){
            console.log(result.responseText);
            var p = $('#check-username');
            p.text("사용할 수 없는 아이디입니다.");
            p.css('color', 'red');
        }
    });

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

