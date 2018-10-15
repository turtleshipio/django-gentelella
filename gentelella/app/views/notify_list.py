from django.shortcuts import render
from app.network.turtleship import APIService
from django.db.models import Sum
from django.views import generic
from django import forms
from app.models import Order
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.views.generic import FormView
from django.views.generic.list import ListView


def notify_retailer_list(request):

    return render(request, 'app/notify_retailer_list.html')


class NotifyListView(ListView):
    model = Order
    context_object_name = 'orders'
    template_name = "app/notify_list.html"
    paginate_by = 10



    def get_context_data(self, *args, **kwargs):
        notify_id = self.kwargs['notify_id']
        context= super(NotifyListView, self).get_context_data(*args, **kwargs)

        special = self.request.GET.get('special')
        print("!!!!")
        print(special)
        if special is None:
            print("??????")
            Order.objects.filter(notify_id=notify_id).update(read=True)

        orders = Order.objects.filter(notify_id=notify_id).order_by("order_id").values('order_id', 'product_name', 'sizencolor', 'count', 'price' )

        paginator = Paginator(orders, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            paged_orders = paginator.page(page)
        except PageNotAnInteger:
            paged_orders = paginator.page(1)
        except EmptyPage:
            paged_orders = paginator.page(paginator.num_pages)

        context['has_previous'] = paged_orders.has_previous()
        context['previous_page_number'] = paged_orders.previous_page_number() if paged_orders.has_previous() else None
        context['number'] = paged_orders.number
        context['has_next'] = paged_orders.has_next()
        context['next_page_number'] = paged_orders.next_page_number() if paged_orders.has_next() else None
        context['num_pages'] = paginator.num_pages
        context['notify_id'] = notify_id
        context['orders'] = paged_orders
        return context
""" 
    def post(self, request, *args, **kwargs):

        notify_id = self.request.POST.get('notify_id', "")
        orders = Order.objects.filter(notify_id=notify_id).order_by("order_id").values('order_id')
        print("??????")
        paginator = Paginator(orders, self.paginate_by)
        page = self.request.GET.get('page')
        return render(request, self.template_name, context={'orders': orders, 'notify_id' : notify_id})"""

