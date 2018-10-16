$("li.list-group-item").click(function(){

    span = $(this).find("span");
    alert(span.attr('id'));
    console.log(span.attr('id'));

    notify_id = span.attr('id');
    window.location.href= "/notify-retailer/" + notify_id;
});