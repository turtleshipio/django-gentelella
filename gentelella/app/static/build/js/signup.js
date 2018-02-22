$('#business-number' ).blur(function() {
    console.log("heyyyy");
    var business_number = $(this).inputmask('remove').val();
    console.log(business_number);
    var p = $('#p-business-number-check');

    var data = {};
    data.business_number = business_number;
    console.log(data);
    sendAjaxForBizNumCheck(data);

});

function sendAjaxForBizNumCheck(data) {

    var csrf = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf);
            }
        }
    });

    $.ajax({
        url : "/check_business_number/",
        type : "POST",
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(data),
        dataType: 'json',
        processData : false,
        contentType: false,
        success : function(result){
            console.log("hiii?");
            exists = result['msg'];
            console.log(exists);
            var p = $('#p-business-number-check');

            if(exists !== 'ok'){
                console.log("working");
                p.text("이미 등록된 번호입니다.");
                p.css('color', 'red');
                console.log(p);
                console.log(p.text());
            } else{
                console.log("let's see...");
                p.text("");
            }

        },

    });

}