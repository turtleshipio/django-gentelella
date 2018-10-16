from django.shortcuts import render
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import Order
from app import custom_db


class NotifyRetailerListView(ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'app/notify_retailer_list.html'

    def get_context_data(self, *args, **kwargs):
        notify_id = self.kwargs['notify_id']
        context = super(NotifyRetailerListView, self).get_context_data(*args, **kwargs)

        orders_dict = {}
        #orders = Order.objects.filter(notify_id=notify_id).order_by("order_id").values("retailer_name", "notify_order_id", "price", "count")


        query = "SELECT retailer_name, ws_name, notify_id, count(*) as count, SUM(price * count) as amt " \
                "FROM orders " \
                "WHERE notify_id = '{notify_id}' " \
                "GROUP BY (retailer_name) " \
                "ORDER BY order_id DESC ".format(notify_id=notify_id)

        orders = custom_db.dict_fetchall(query)


        context['orders'] = orders
        context['notify_id'] = notify_id
        context['ws_name'] = orders[0]['ws_name']
        return context
