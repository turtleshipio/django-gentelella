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

$("button[id^='btn-edit-ws-']").click(function(event){
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
                var select_floor = null;

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

$(document).ready(function(){
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
    });

    var index = ['updated_time', 'ws_name', 'building', 'floor', 'location', 'col' ];

    $.ajax({
        url : "/manage_ws/wsbytcorg/" ,
        type : "post",
        contentType : 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data){
            var table = $(".display tbody")
            table.empty();

            var html = ""

            for(var i=0; i < data.length; i++){

                html = "<tr>"
                var flag = false;
                for(key in data[i]){
                    console.log(key);
                }
                for(var j=0; j < index.length; j++){
                    for(key in data[i]){
                        if(index[j] === key){
                            if(key === "ws_name"){
                                html = html + "<td class='text-center'><span><strong>" + data[i][key] + "</strong></span></td>";
                            } else{
                                html = html + "<td class='text-center'><span>" +data[i][key] + "</span></td>";
                            }
                            flag = true;
                        }

                    }
                }

                 var empty = "<td class='text-center'><span></span></td>";
                    if(!flag){
                        html = html+empty;
                    }
                    html = html + empty;
                html = html + "</tr>"
                table.append(html);
            }







            var tableOptions = {
            "language":{
                "info" : "_TOTAL_ 건의 결과중 _START_ 에서 _END_ ",
                "lengthMenu" : "_MENU_ 건씩 검색",
                "zeroRecords": "검색결과가 없습니다.",
                "search" : "검색:\t",
                "paginate": {
                    "first" : "처음",
                    "last" : "마지막",
                    "next" : "다음",
                    "previous" : "이전",
                },
                 "scroller": {
                    loadingIndicator: true
                },
                "loadingRecords" : "잠시만 기다려주세요...",
                "aria" : {
                    "sortAscending" : ": 오름차순",
                    "sortDescending" : ": 내림차순",
                    "paging":true,
                },
                "deferRender":true,


            },
        };
       },

    });




});



