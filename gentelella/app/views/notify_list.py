from django.shortcuts import render
from app.network.turtleship import APIService
from django.db.models import Sum
from django.views import generic
from app.models import Orders, Credits
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger
from app.utils import getYesterdayDateAt11pm
import logging
from django.utils.decorators import method_decorator
from app.decorators import require_token
from app import utils


class NotifyListView(generic.ListView):
    model = Orders
    context_object_name = 'hello'
    template_name = "app/notify_list.html"
    paginate_by = 10


    def get(self, request, notify_id):
        orders = Orders.objects.filter(notify_id=notify_id).order_by("order_id")
        paginator = Paginator(orders, self.paginate_by)
        page = self.request.GET.get('page')

        return render(request, self.template_name, context={'orders': orders})


    def post(self, request, *args, **kwargs):
        print("#############################")
        print("#############################")
        print("#############################")
        print("#############################")
        print("#############################")
        print("#############################")


        notify_id = self.request.POST.get('notify_id', "")
        orders = Orders.objects.filter(notify_id=notify_id).order_by("order_id")
        paginator = Paginator(orders, self.paginate_by)
        page = self.request.GET.get('page')
        return render(request, self.template_name, context={'orders': orders})

        for order in orders:
            print("#############################")
            print("#############################")
            print("#############################")
            print("#############################")
            print("#############################")
            print("#############################")
            print(order.product_name)
            print(order.count)


        """ 
        try:
            paged_credits = paginator.page(page)
        except PageNotAnInteger:
            paged_credits = paginator.page(1)
        except EmptyPage:
            paged_credits = paginator.page(paginator.num_pages)
            """

        #   self.context['orders'] = orders
        print(orders)

        return render(request, self.template_name, context={'orders': orders})

