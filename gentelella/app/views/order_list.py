from django.shortcuts import render
from app.network.turtleship import APIService
from django.views import generic
from app.models import Orders
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger
from app.utils import getYesterdayDateAt11pm
from django.utils.decorators import method_decorator
from app.decorators import require_token
from app import utils


class OrderListView(generic.ListView):
    model = Orders
    context_object_name = 'orders'
    template_name = "app/order_list.html"
    paginate_by = 10


    #@method_decorator(require_token())
    def dispatch(self, *args, **kwargs):
        return super(OrderListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        token = self.request.session['token']
        token = utils.get_decoded_token(token)
        print(token['retailer_id'])
        orders = Orders.objects.filter(retailer_id=token['retailer_id'], is_deleted='false').order_by('-order_id')

        paginator = Paginator(orders, self.paginate_by)
        page = self.request.GET.get('page')
        context = super(OrderListView, self).get_context_data(**kwargs)


        context['token'] = utils.get_decoded_token(token)

        try:
            paged_orders = paginator.page(page)
        except PageNotAnInteger:
            paged_orders = paginator.page(1)
        except EmptyPage:
            paged_orders = paginator.page(paginator.num_pages)

        context['orders'] = paged_orders
        context['retail_user'] = utils.get_retail_user_from_token(token)

        return context
