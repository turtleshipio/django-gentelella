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
        print("BBBBBBBBBBBBBBBBB")
        notify_id = self.kwargs['notify_id']
        context = super(NotifyRetailerListView, self).get_context_data(*args, **kwargs)

        orders_dict = {}
        orders = Order.objects.filter(notify_id=notify_id).order_by("order_id").values("retailer_name", "notify_order_id", "price", "count")

        for order in orders:
            retailer = order['retailer_name']
            amt = order['price'] * order['count']
            if retailer in orders_dict:
                orders_dict[retailer]['amt'] += amt
                orders_dict[retailer]['count'] += 1
            else:
                orders_dict[retailer] = {}
                orders_dict[retailer]['amt'] = amt
                orders_dict[retailer]['count'] = 1

        context['orders'] = orders
        context['orders_dict'] = orders_dict
        return context
