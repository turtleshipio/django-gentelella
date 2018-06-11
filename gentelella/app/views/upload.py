from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from app.forms import DocumentForm
from app.decorators import require_token, require_login
from app import utils
from app.excel import UploadManager
from app.models import  Order, RetailerPickteam
from app import common
from django.db import transaction
from app.kakao import OrderSubmitManager
import json

import io
import xlrd


@require_login()
@require_http_methods(['GET', 'POST'])
def bulk_orders(request):
    context= {
        'retailer_name' : None,
        'order' : None
    }


    retailer = request.user.groups.filter(name="retailer_group")

    if len(retailer) > 0:
        context['retailer_name'] = retailer[0].name

    if request.method == "GET":

        return render(request, 'app/form_upload.html', context=context)

    if request.method == "POST":

        if request.is_ajax():

            data_js = json.loads(request.body.decode('utf-8'))

            orders_js = data_js[0]['orders']
            retailer_name = ""
            try:
                retailer_name = data_js[0]['retailer_name']
            except:
                pass


            manager = OrderSubmitManager()
            result = manager.create_orders_from_js(orders_js, request.user.username)

            if result is True:

                phones = ['01036678070']
            notifies = manager.notifies

            for ws_name in notifies:
                notify_id = notifies[ws_name]['notify_id']
                order_id = notify_id[:7]
                prd1 = notifies[ws_name]['prd1']
                prd_count = int(notifies[ws_name]['prd_count']) - 1
                phn = notifies[ws_name]['phn']

                sender.set_msg(order_id=order_id, retailer_name=retailer_name,
                               prd1=prd1, prd_count=prd_count,
                               notify_id=notify_id)

                if phn not in phones:
                    phones.append(phn)
                for phn in phones:
                    sender.send_kakao_msg(phn)
                sender.clear()
                phones = ['01036678070', '01088958454']


                return HttpResponse("Ok")

@require_login()
@require_http_methods(['GET', 'POST'])
def modal_view(request):

    if request.method == "POST":

        is_retailer = common.check_group(request.user, 'retailer_group')

        retailer_name = ""

        if 'retailer_name' in request.POST:
            retailer_name = request.POST['retailer_name']

        file = request.FILES['excel_file']


        manager = UploadManager()
        manager.set_file(file)
        manager.validate()

        orders, success, msg = manager.extract()

        if success:
            return render(request, 'app/excel_modal.html', context={'orders': orders, 'retailer_name': retailer_name, 'msg':None})
        else:
            return render(request, 'app/excel_modal.html', context={'orders': None, 'retailer_name':None, 'msg':msg})



