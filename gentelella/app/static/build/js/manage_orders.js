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
};

function isWhiteSpace(str){
    return str.replace(/^\s+|\s+$/gm,'').length == 0;
};

$('button#btn-confirm-upload').click(function(event){

    console.log("here!!!");
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
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
    });

    $.ajax({
        url : "/upload_bulk/",
        type : "POST",
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify([data]),
        dataType: 'text',
        success : function(result){
            window.location.href = "/manage_orders/";
        },
        error : function(result){
            alert("에러가 생겼습니다.");
        }


    });
});


$('form#excel-modal').on('submit', function(event){
    event.preventDefault();
    var formData = new FormData(this);

    var retailer_name = $('#select-retailer option:selected').val();
    formData.append('retailer_name', retailer_name);



     $.ajax({
        url : "/excel_modal/",
        type : "POST",
        data : formData,
        processData : false,
        contentType: false,
        success : function(response, data){

            $('#excel_modal').find('.modal-body').html(response);
            $('#excel_modal').modal('show');

        },

    });

});



$('button#submit-edit-ws-modal').click(function(event){
    var data= {};
    var counter = $(this).val();
    var building = $('select#select-buildings-edit-ws-'+counter);
    var floor = $('select#floor-edit-ws-'+counter);


    data.ws_name = $('input#edit-ws-name-1').val();
    data.building = building.val();
    data.floor = $('select#floor-edit-ws-'+counter).val();
    data.location = $('input#edit-location-'+counter).val();
    data.col = $('input#edit-col-'+counter).val();
    data.ws_phone= $('input#edit-ws-phone-'+counter).val();


    if(isWhiteSpace(data.ws_name)){
        alert("도매명을 입력해주세요");
        return;
    }

    if (!building.find('option:not(:first)').is(':selected')){
        alert('상가를 선택해주세요');
        return;
    }

    if (!floor.find('option:not(:first)').is(':selected')){
        alert('도매점의 층을 선택해주세요');
        return;
    }

    if(isWhiteSpace(data.location)){
        alert('도매점의 호수를 선택해주세요');
        return;
    }

    if(isWhiteSpace(data.ws_phone)){
        alert('핸드폰 번호를 입력해주세요');
        return;

    }


    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
    });

    $.ajax({
        url : "/edit_wsbyuser/",
        type : "PUT",
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify([data]),
        dataType: 'text',
        success : function(result){
            window.location.href = "/manage_ws/";
        },
        error : function(result){
            alert("에러가 생겼습니다.");
        },



    });


});

$("button#submit-order-format").click(function(event){

    var retailer_name = $("input#input-retailer-name").val();
    if (retailer_name == null || retailer_name === ""){
        alert("소매를 먼저 선택해주세요");
        return;
    }
    alert("heyhey");

    var counter = $(this).val();
    var select_buildings_id = "select#select-buildings-edit-ws-" + counter;
    var select_building = $(select_buildings_id);

    var building_org = $('p#edit-ws-building-'+counter).text();
    var building = $(select_buildings_id).val(building_org);
    data = {};
    data.building = building_org;



    var csrftoken = getCookie('csrftoken');

         $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
         });

         $.ajax({
            url : "/manage_ws/buildings/",
            type : "POST",
            contentType : 'application/json; charset=utf-8',
            data: JSON.stringify([data]),
            dataType : "json",
            success:function(result){

                select_floor_id= "select#floor-edit-ws-" + counter;
                select_floor = $(select_floor_id);
                select_floor.attr("readonly", false);
                select_floor.find('option:not(:first)').remove();

                var floors = result['floors'];

                for(var key in floors){
                    floor = floors[key];
                    var option = $("<option></option>");
                    option.text(floor);
                    option.val(floor);
                    select_floor.append(option);
                }

                var option_text = 'option[value="' + building_org + '"]';
                select_floor.find(option_text).val();
                select_building.find('option').each(function(index, element){
                    if(element.value === building_org){
                        element.attr('selected','selected');
                    }
                });

            },
            error:function(result){
                alert("에러가 생겼습니다.");
            }
        });
});

$("select[id^='select-retailer']").on('change', function(){
    var retailer_name = $("#select-retailer option:selected").val();

    data = {};
    data.retailer_name = retailer_name;

     $.ajax({
            url : "/manage_orders/formats/",
            type : "GET",
            contentType : 'application/json; charset=utf-8',
            data: {
                "retailer_name" : retailer_name
            },
            dataType: "json",
            success:function(result){
                $('input#input-retailer-name').val(retailer_name);
                $('input#order-fmt-ws-name').val(result['fmt_ws_name']);
                $('input#order-fmt-product-name').val(result['fmt_product_name']);
                $('input#order-fmt-sizeNcolor').val(result['fmt_sizeNcolor']);
                $('input#order-fmt-color').val(result['fmt_color']);
                $('input#order-fmt-count').val(result['fmt_count']);
                $('input#order-fmt-price').val(result['fmt_price']);
                $('input#order-fmt-request').val(result['fmt_request']);
                $('input#order-format').val(result['str']);
            },
            error:function(result){
               alert("에러가 생겼습니다.");
            }
        });
});

$('button#btn-delete-ws').click(function(event){
    id = $(this).val();
    data = {}
    data.id = id;
    var tr_id = "#tr-ws-list" + id;
    var a_id = "#a-ws-name-list" + id;
    var ws_name = $(a_id).text();
    var msg = "다음 도매를 정말 삭제하시겠습니까?:\t" + ws_name;

    if(confirm(msg)){
        var csrftoken = getCookie('csrftoken');

         $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
         });

        $.ajax({
            url : "/delete_wsbyuser/",
            type : "PUT",
            contentType : 'application/json; charset=utf-8',
            data: JSON.stringify([data]),
            dataType: 'text',
            success:function(result){

                $(tr_id).remove();
            },
            error:function(result){
                alert("해당 도매를 삭제하는데 실패하였습니다.");
            }
        });
    }

});

$('button#btn-add-ws-modal').click(function(event){


    var data= {};
    data.ws_name = $('input#ws_name').val();
    if(isWhiteSpace(data.ws_name)){
        alert("도매명을 입력해주세요");
        return;
    }
    var building = $('select#select-buildings-add-ws-0');
    if (!building.find('option:not(:first)').is(':selected')){
        alert('상가를 선택해주세요');
        return;
    }
    data.building = building.val();
    var floor = $('select#floor-add-ws-0');
    if (!floor.find('option:not(:first)').is(':selected')){
        alert('도매점의 층을 선택해주세요');
        return;
    }
    data.floor= floor.val();
    var location = $('input#location');
    data.location = location.val();
    if(isWhiteSpace(data.location)){
        alert('도매점의 호수를 선택해주세요');
        return;
    }

    data.col = $('input#col').val();

    data.ws_phone= $('input#ws_phone').val();
    if(isWhiteSpace(data.ws_phone)){
        alert('핸드폰 번호를 입력해주세요');
        return;

    }
    var selected_floor = $('select#floor-add-ws-0');
    var is_not_first = selected_floor.find('option:not(:first)').is(':selected');
    var csrftoken = getCookie('csrftoken');


    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
    });

    $.ajax({
        url : "/manage_ws/",
        type : "POST",
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify([data]),
        dataType: 'text',
        success : function(result){
            window.location.href = "/manage_ws/";
        }, error : function(result){
            alert("새로운 도매를 추가할때 문제가 생겼습니다.");
        }


    });
});