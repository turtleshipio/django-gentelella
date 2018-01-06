from django.shortcuts import render
from app.network.turtleship import APIService
from django.views import generic
from app.models import *
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger
from app.utils import getYesterdayDateAt11pm
from django.utils.decorators import method_decorator
from app.decorators import *
from app import utils


class ManageWSListView(generic.ListView):
    model = Ws
    context_object_name = 'ws'
    template_name = "app/manage_ws.html"
    paginate_by = 10


    @method_decorator(can_manage_ws())
    def dispatch(self, *args, **kwargs):
        return super(ManageWSListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        token = self.request.session['token']
        token = utils.get_decoded_token(token)

        acc_type = token['acc_type']

        orders = []
        if acc_type == "retailer":
            retailer_name = token['retailer_name']
            orders = Orders.objects.filter(retailer_name=retailer_name).order_by('-order_id').values('order_id', 'ws_name', 'created_time','retailer_name',
                                                                           'count', 'price', 'status')


        if acc_type == "pickup":
            pickteam_id = token['pickteam_id']
            orders = Orders.objects.filter(pickteam_id=pickteam_id).order_by('-order_id').values('order_id', 'ws_name', 'created_time', 'count', 'retailer_name',
                                                                 'price', 'status')


        paginator = Paginator(orders, self.paginate_by)
        page = self.request.GET.get('page')
        context = super(ManageWSListView, self).get_context_data(**kwargs)


        context['token'] = utils.get_decoded_token(token)

        try:
            paged_orders = paginator.page(page)
        except PageNotAnInteger:
            paged_orders = paginator.page(1)
        except EmptyPage:
            paged_orders = paginator.page(paginator.num_pages)

        context['orders'] = paged_orders
        t_user = utils.get_user_from_token(token)
        context['t_user'] = t_user
        print(t_user.acc_type)
        #context['retail_user'] = utils.get_retail_user_from_token(token)

        return context