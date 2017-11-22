from django.shortcuts import render
from app.network.turtleship import APIService
from django.views import generic
from app.models import Orders
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger
from app.utils import getYesterdayDateAt11pm


class OrderListView(generic.ListView):
    model = Orders
    context_object_name = 'orders'
    template_name = "app/order_list.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        orders = Orders.objects.filter(retailer_idx=0, is_deleted='false')
        paginator = Paginator(orders, self.paginate_by)
        page = self.request.GET.get('page')
        context = super(OrderListView, self).get_context_data(**kwargs)

        try:
            paged_orders = paginator.page(page)
        except PageNotAnInteger:
            paged_orders = paginator.page(1)
        except EmptyPage:
            paged_orders = paginator.page(paginator.num_pages)

        context['orders'] = paged_orders

        return context

