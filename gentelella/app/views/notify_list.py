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
from django.views.generic.list import ListView

class NotifyListForm(forms.Form):
    order_id = forms.RadioSelect()


class NotifyListView(ListView):
    model = Order
    context_object_name = 'orders'
    template_name = "app/notify_list.html"
    paginate_by = 10
    allow_empty = False



     #   self.object = Order.objects.filter(notify_id=notify_id).order_by("-order_id")
      #  return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        notify_id = self.kwargs['notify_id']
        context= super(NotifyListView, self).get_context_data(*args, **kwargs)
        context['orders'] = Order.objects.filter(notify_id=notify_id).order_by("order_id")
        return context

    def post(self, request, *args, **kwargs):


        notify_id = self.request.POST.get('notify_id', "")
        orders = Order.objects.filter(notify_id=notify_id).order_by("order_id")
        paginator = Paginator(orders, self.paginate_by)
        page = self.request.GET.get('page')
        return render(request, self.template_name, context={'orders': orders, 'notify_id' : notify_id})

