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



$("button#submit-order-format").click(function(event){

    var counter = $(this).val();
    var retailer_name_id = "input#input-retailer-name-" + counter;
    var retailer_name = $(retailer_name_id).val();

    var fmt_ws_name_id = "input#order-fmt-ws-name-" + counter;
    var fmt_product_name_id = "input#order-fmt-product-name-" + counter;
    var fmt_sizencolor_id = "input#order-fmt-sizencolor-" + counter;
    var fmt_color_id = "input#order-fmt-color-" + counter;
    var fmt_price_id = "input#order-fmt-price-" + counter;
    var fmt_count_id = "input#order-fmt-count-" + counter;
    var fmt_request_id = "input#order-fmt-request-" + counter;


    data = {};
    data.retailer_name      = retailer_name;
    data.fmt_ws_name        = $(fmt_ws_name_id).val();
    data.fmt_product_name   = $(fmt_product_name_id).val();
    data.fmt_sizencolor     = $(fmt_sizencolor_id).val();
    data.fmt_color          = $(fmt_color_id).val();
    data.fmt_price          = $(fmt_price_id).val();
    data.fmt_count          = $(fmt_count_id).val();
    data.fmt_request        = $(fmt_request_id).val();

    var csrftoken = getCookie('csrftoken');

         $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
         });

         $.ajax({
            url : "/manage_retailers/",
            type : "PUT",
            contentType : 'application/json; charset=utf-8',
            data: JSON.stringify([data]),
            dataType : "text",
            success:function(result){
                var modal_id = "div#modal-" + counter;
                $(modal_id).modal('hide');
                alert("수정 되었습니다.");

            },
            error:function(result){
                alert("에러가 생겼습니다.");
            }
        });
});

$("select[id^='select-buildings-']").on('change', function(){
    var counter = $(this).attr('name');
    var building = $(this).val();

    var select_buildings_id = $(this).prop('id');
    var option_id = "";
    var select_buildings_add_id = "select-buildings-add-ws-" + counter;
    var select_buildings_edit_id = "select-buildings-edit-ws-" + counter;


    if (select_buildings_id === select_buildings_add_id){
        option_id = 'option#option-default-add-ws-' + counter;
    }
    else if(select_buildings_id === select_buildings_edit_id){
        option_id = 'option#option-default-edit-ws-' + counter;
    } else {
        option_id = "";
    }

    var option_default = $(option_id);

    data = {};
    data.building = building;

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


                var floor_add_id = "select#floor-add-ws-" + counter;
                var floor_edit_id = "select#floor-edit-ws-" + counter;
                var select_floor =null;

                if (select_buildings_id === select_buildings_add_id){
                    select_floor = $(floor_add_id);
                }
                else if(select_buildings_id === select_buildings_edit_id){
                    select_floor = $(floor_edit_id);
                } else {
                    select_floor = null;
                }

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

function plot_data(){

    var data = [];
    //console.log(orders_count);
    console.log(orders_count.length);
    for (var i = 0; i < orders_count.length; i++){
        console.log(new Date(orders_count[i][0]).getTime(), orders_count[i][1]);
        data.push({
            x: new Date(orders_count[i][0]).getTime(),
            y: orders_count[i][1]
        });
    }

    var ctx = $("#super-chart");

    console.log(ctx);

    var chart = new Chart(ctx, {
        type: 'line',
        label: "누적 주문건수",
        lines: {
            fillColor: "rgba(150, 202, 89, 0.12)"
        },
        points: {
            fillColor: "#fff"
        },
        }], chart_plot_02_settings);

    })


}

var flot_settings = {
}

function init_flot(){
    $.plot(
        $("#flot-super-chart"),
        [{
            type: 'line',
            label: "누적 주문건수",
            lines: {
                fillColor: "rgba(150, 202, 89, 0.12)"
            },
            points: {
                fillColor: "#fff"
            },
        }], flot_settings);

    )
}


