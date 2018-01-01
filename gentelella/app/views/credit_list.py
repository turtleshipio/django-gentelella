from django.shortcuts import render
from app.network.turtleship import APIService
from django.db.models import Sum
from django.views import generic
from app.models import *
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger
from app.utils import getYesterdayDateAt11pm
import logging
from django.utils.decorators import method_decorator
from app.decorators import require_token
from app import utils

class CreditListView(generic.ListView):
    model = Credits
    context_object_name = 'credits'
    template_name = "app/credit_list.html"
    paginate_by = 10

    @method_decorator(require_token())
    def dispatch(self, *args, **kwargs):
        return super(CreditListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):

        l = logging.getLogger('django.db.backends')
        l.setLevel(logging.DEBUG)
        l.addHandler(logging.StreamHandler())

        token = self.request.session['token']
        token = utils.get_decoded_token(token)

        acc_type = token['acc_type']
        retailer_id = []
        if acc_type == "retailer":
            retailer_id = retailer_id.append(token['retailer_id'])

        if acc_type == "pickup":
            pickteam_id = token['pickteam_id']
            retailer_id = Retailer.objects.filter(pickteam_id=pickteam_id).values_list('retailer_id', flat=True)


        credits = Credits.objects.filter(retailer_id=retailer_id, order_of_credits__oos='true') \
            .annotate(amount=Sum('order_of_credits__price')) \
            .order_by('-created_time')

        paginator = Paginator(credits, self.paginate_by)
        page = self.request.GET.get('page')
        context = super(CreditListView, self).get_context_data(**kwargs)


        try:
            paged_credits = paginator.page(page)
        except PageNotAnInteger:
            paged_credits = paginator.page(1)
        except EmptyPage:
            paged_credits = paginator.page(paginator.num_pages)

        context['credits'] = credits
        context['t_user'] = utils.get_user_from_token(token)

        return context

