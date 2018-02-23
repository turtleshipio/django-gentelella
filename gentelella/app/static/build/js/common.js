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

function isNumeric(str) {
  var code, i, len;

  for (i = 0, len = str.length; i < len; i++) {
    code = str.charCodeAt(i);

    if (!(code > 47 && code < 58)) {
      return false;
    }
  }
  return true;
};

function isWhiteSpace(str){
    return (str.length === 0 || !str.trim());
}