from django.shortcuts import render
from app.network.turtleship import APIService
from django.db.models import Sum
from django.views import generic
from app.models import *
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger
from app.utils import getYesterdayDateAt11pm
import logging
from django.utils.decorators import method_decorator
from app import utils
from django.contrib.auth.decorators import  login_required

class CreditListView(generic.ListView):
    model = Credits
    context_object_name = 'credits'
    template_name = "app/credit_list.html"
    paginate_by = 10

    def dispatch(self, *args, **kwargs):
        return super(CreditListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):

        credits = Credits.objects.filter(retailer_id=-1) \
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

        return context

