$("li.list-group-item").click(function(){

    span = $(this).find(".retailer_name");
    retailer_name = span.text();
    notify_id = span.attr('id');
    window.location.href= "/notify-retailer/" + notify_id + "?retailer_name=" + retailer_name;
});