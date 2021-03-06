from django.views.generic.list import ListView
from django.http import *
from app.models import *
from braces.views import GroupRequiredMixin
import json


class TCRetailersListView(ListView):
    model = TCRetailer
    context_object_name = 'retailers'
    template_name = "app/manage_retailers.html"
    group_required = ["pickteam_group", u"staff"]
    login_url = '/'
    paginate_by = 10

    def get_queryset(self):
        org = TCOrg.objects.get(main_user=self.request.user)
        return TCRetailer.objects.filter(pickteam=org)

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page')

    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden
        if not request.is_ajax():
            return HttpResponseBadRequest

        data_js = json.loads(request.body.decode('utf-8'))[0]

        retailer_name = data_js['retailer_name']
        fmt_ws_name = data_js['fmt_ws_name']
        fmt_product_name = data_js['fmt_product_name']
        fmt_sizencolor= data_js['fmt_sizencolor']
        fmt_color= data_js['fmt_color']
        fmt_price= data_js['fmt_price']
        fmt_count= data_js['fmt_count']
        fmt_request = data_js['fmt_request']

        try:
            pickteam = TCPickteam.objects.get(main_user=self.request.user)
            retailer = TCRetailer.objects.get(pickteam=pickteam, org_name=retailer_name)
            format = retailer.order_format

            format.fmt_ws_name = fmt_ws_name
            format.fmt_product_name = fmt_product_name
            format.fmt_sizencolor = fmt_sizencolor
            format.fmt_color = fmt_color
            format.fmt_price = fmt_price
            format.fmt_count = fmt_count
            format.fmt_request = fmt_request
            format.save()
            response = HttpResponse()
            response.status_code= 200
            return response
        except Exception as e:
            response = HttpResponse()
            response.status_code=500
            return response

