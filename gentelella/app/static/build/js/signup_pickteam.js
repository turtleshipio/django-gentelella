$('#business-number' ).blur(function() {
    console.log("heyyyy");
    var temp = jQuery.extend({}, $(this));
    var business_number = temp.inputmask('remove').val();
    console.log(business_number);
    var p = $('#p-business-number-check');

    var data = {};
    data.business_number = business_number;
    console.log(data);
    sendAjaxForBizNumCheck(data);

});

$('div#duplicate-username').click(function(event){
    console.log("it works!!");
    var data= {};
    var username = "";
    username = $('#username').val();
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
                var state = $("input#username_state")
                state.attr("value", "good")

            } else{
                var state = $("input#username_state")
                p.text("사용할 수 없는 아이디입니다.");
                p.css('color', 'red');
                state.attr("value", "bad")
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





function sendAjaxForUsernameFormCheck(data) {

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

            if (result['msg'] !== "ok"){
                alert("중복된 아이디입니다.\n중복확인을 눌러 확인해주세요");
                return false;
            }

        },
        error : function(result){
            alert("아이디에 이상이 있습니다. 다시 시도해주세요");
            return false;
        }


    });

}

// Need this to know which form ahs been clicked
$("form button[type=submit]").click(function() {
        $("button[type=submit]", $(this).parents("form")).removeAttr("clicked");
        $(this).attr("clicked", "true");
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

$('#signup-form').submit(function(e){
    e.preventDefault();
    var button = $("button[type=submit][clicked=true]").val(); //check if cancel form submission

    if (button === "cancel"){
        window.location.replace("/");
        return false;
    }
    var username = $('#username').val();
    var password = $('#password').val();
    var password_check = $('#password-check').val();
    var full_name = $('#full_name').val();
    var phone = $('#phone').inputmask('remove').val();


    if (username.length < 4 || !isAlphaNumeric(username)){
        alert("아이디를 수정해주세요");
        return false;
    }

    if (isWhiteSpace(password) || password.length < 8){
        alert("비밀번호는 8자리 이상이어야 합니다.");
        return false;
    }

    if (password !== password_check){
        alert("비밀번호가 일치하지 않습니다.");
        return false;
    }

    if (isWhiteSpace(full_name)){
        alert("이용자 이름을 확인해주세요");
        return false;
    }

    if (!isNumeric(phone) || phone.length < 10 || phone.length > 11){
        alert("전화번호를 확인해주세요");
        return false;
    }


    var data = {};
    data.username = username;
    data.password = password;
    data.full_name = full_name;
    data.phone = phone;

    $.ajax({
        url : "/signup-pickteam/",
        type : "POST",
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(data),
        dataType: 'json',
        processData : false,
        contentType: false,
        success : function(result){
            alert("회원가입성공");
            window.location.replace("/home/");


        },
        error : function(result){
             window.location.replace("/home/");
        }

    });



    return true;





});

$(document).ready(function(){

    var stepContainer = $("#step-2");

    stepContainer.css("height", 200);

    $("#wizard").smartWizard({
        onLeaveStep:leaveStepCallBack,
        onFinish:onFinishCallback,
    });
});

function onFinishCallback(obj, context){

    var csrf = getCookie('csrftoken');
    var username = $('#username').val();
    var password = $('#password').val();
    var full_name = $('#full_name').val();
    var phone = $('#phone').inputmask('remove').val();
    var data = {};

    data.username = username;
    data.password= password;
    data.full_name= full_name;
    data.phone= phone;

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf);
            }
        }
    });

      $.ajax({
        url : "/signup-pickteam/",
        type : "POST",
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(data),
        processData : false,
        contentType: false,
        success : function(result){
            window.location.replace("/signup-pickteam-done")

        },
        error : function(result){
        }

    });




}
function leaveStepCallBack(obj, context){
    return usernameCheck() && passwordCheck();
}

function passwordCheck(){
    var password = $('#password').val();
    var password_check = $('#password-check').val();
    var p = $('#p-password-check');


    if (password === password_check){
        if (password.length < 8){
            return false;
        } else {
            return true;
        }
    } else{
        return false;
    }
}

function usernameCheck(){

     var data= {};
     var username = "";
     username = $('#username').val();
     data.username = username;


     if (username.length < 4 || !isAlphaNumeric(username)){
        alert("아이디를 수정해주세요");
        return false;
     } else{
        var exists = $("input#username_state").val();
        if(exists ==="bad"){
            alert("중복된 아이디입니다. 중복확인을 눌러 확인해주세요")
            return false;
        } else{
            return true;
        }
     }
     return false;
}


$("p#otp").click(function(){


    var csrf = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf);
            }
        }
    });

      $.ajax({
        url : "/pyotp/",
        type : "POST",
        contentType: 'application/json; charset=utf-8',
        processData : false,
        contentType: false,
        success : function(result){
            window.href.location="/signup-pickteam-done/"

        },
        error : function(result){
        }

    });
});


