from django.shortcuts import render
from app.network.turtleship import APIService
from django.db.models import Sum
from django.views import generic
from django import forms
from app.models import Order, Credits
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.views.generic import FormView
from app.forms import CreditForm

from app.utils import getYesterdayDateAt11pm
import logging
from django.utils.decorators import method_decorator
from app.decorators import require_token
from app import utils


class NotifyListForm(forms.Form):
    order_id = forms.RadioSelect()


class NotifyListView(SingleObjectMixin, FormView):
    model = Order
    context_object_name = 'orders'
    template_name = "app/notify_list.html"
    paginate_by = 10
    form_class = CreditForm
    allow_empty = False


    def get(self, request, notify_id, *args, **kwargs):

        self.object = Order.objects.filter(notify_id=notify_id).order_by("-order_id")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = self.object
        return context

    def post(self, request, *args, **kwargs):


        notify_id = self.request.POST.get('notify_id', "")
        orders = Order.objects.filter(notify_id=notify_id).order_by("order_id")
        paginator = Paginator(orders, self.paginate_by)
        page = self.request.GET.get('page')
        return render(request, self.template_name, context={'orders': orders, 'notify_id' : notify_id})



        #   self.context['orders'] = orders
        print(orders)

        return render(request, self.template_name, context={'orders': orders})





class NotifyListPost(FormMixin, generic.ListView):
    form_class =  NotifyListForm
    template_name = "app/notify_list.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object

