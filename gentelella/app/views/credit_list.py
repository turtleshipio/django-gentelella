from django.shortcuts import render
from app.network.turtleship import APIService
from django.db.models import Sum
from django.views import generic
from app.models import Orders, Credits
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger
from app.utils import getYesterdayDateAt11pm
import logging

class CreditListView(generic.ListView):
    model = Credits
    context_object_name = 'orders'
    template_name = "app/credit_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):

        l = logging.getLogger('django.db.backends')
        l.setLevel(logging.DEBUG)
        l.addHandler(logging.StreamHandler())

        credits = Credits.objects.filter(retailer_idx=0, order_of_credits__oos='true')\
            .annotate(amount=Sum('order_of_credits__price'))\
            .order_by('created_time')

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


        return context

