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
    var retailer_name = $('#retailer-name').val();
    var temp = jQuery.extend({}, $('#business-number'));
    var business_number = temp.inputmask('remove').val();
    var name = $('#name').val();
    var phone = $('#phone').inputmask('remove').val();


    if (username.length < 4 || !isAlphaNumeric(username)){
        alert("아이디를 수정해주세요");
        return false;
    }

    console.log("1");
    if (isWhiteSpace(password) || password.length < 8){
        alert("비밀번호는 8자리 이상이어야 합니다.");
        return false;
    }
    console.log("2");
    if (password !== password_check){
        alert("비밀번호가 일치하지 않습니다.");
        return false;
    }
    console.log("3");
    if (isWhiteSpace(retailer_name)){
        alert("소매명을 확인해주세요");
        return false;
    }
    console.log("4");
    if (isWhiteSpace(name)){
        alert("대표자 이름을 확인해주세요");
        return false;
    }
    console.log("5");
    if (!isNumeric(business_number)|| business_number.length !== 10 ){
        alert("사업자 등록번호를 확인해주세요");
        return false;
    }
    console.log("6");
    if (!isNumeric(phone) || phone.length < 10 || phone.length > 11){
        alert("전화번호를 확인해주세요");
        return false;
    }


    console.log("7");

    /*
    if (username.length >= 4 || isAlphaNumeric(username)){
        console.log("x");
        data = {};
        data.username = username;
        sendAjaxForUsernameFormCheck(data);
        return false;
    }*/
    console.log("8");
    //if (isNumeric(business_number)|| business_number.length === 10 ){
    //    sendAjaxForUsernameFormCheck(username);
    //    return false;
    //}

     window.location.replace("/");
     return true;





});
