from django.shortcuts import render
from app.network.turtleship import APIService
from django.views import generic
from app.models import *
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger
from app.utils import getYesterdayDateAt11pm
from django.utils.decorators import method_decorator
from app.decorators import require_token
from app import utils


class OrderListView(generic.ListView):
    model = Orders
    context_object_name = 'orders'
    template_name = "app/order_list.html"
    paginate_by = 20


    #@method_decorator(require_token())
    def dispatch(self, *args, **kwargs):
        return super(OrderListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        token = self.request.session['token']
        token = utils.get_decoded_token(token)

        acc_type = token['acc_type']

        orders = []
        if acc_type == "retailer":
            retailer_name = token['retailer_name']
            orders = Orders.objects.exclude(is_deleted="true").filter(retailer_name=retailer_name).order_by('-order_id').values('order_id', 'ws_name', 'created_time','retailer_name',
                                                                           'count', 'price', 'status')


        if acc_type == "pickup":
            pickteam_id = token['pickteam_id']
            orders = Orders.objects.exclude(is_deleted="true").filter(pickteam_id=pickteam_id).order_by('-order_id').values('order_id', 'ws_name', 'created_time', 'count', 'retailer_name',
                                                                 'price', 'status')

        paginator = Paginator(orders, self.paginate_by)
        page = self.request.GET.get('page')
        context = super(OrderListView, self).get_context_data(**kwargs)



        context['token'] = utils.get_decoded_token(token)
        context['ws_perm'] = None
        print("!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(str(paginator.num_pages))
        num_pages = paginator.num_pages
        try:
            paged_orders = paginator.page(page)
        except PageNotAnInteger:
            paged_orders = paginator.page(1)
        except EmptyPage:
            paged_orders = paginator.page(paginator.num_pages)

        context['orders'] = paged_orders
        t_user = utils.get_user_from_token(token)
        context['t_user'] = t_user
        context['num_pages'] = num_pages
        print(t_user.acc_type)
        #context['retail_user'] = utils.get_retail_user_from_token(token)

        return context
