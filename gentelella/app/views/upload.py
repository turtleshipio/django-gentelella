from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from app.forms import DocumentForm
from app.decorators import require_token, require_login
from app import utils
from app.excel import OrderExcelValidator
from app.models import *
from app import common
from django.db import transaction
from app.kakao import OrderCreator, KakaoNotifySender
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
            phones = []

            retailer_name = ""
            pickteam = None

            is_retailer = common.check_group(request.user, 'retailer_group')

            if is_retailer:
                retailer = TCRetailer.objects.get(main_user=request.user)
                retailer_name = retailer.org_name

                group = request.user.groups.get(name='retailer_group')
                pickteam = retailer.pickteam.all()[0] # technically should be foreign key instead of n:n. Just for now.

            else: # if pickteam
                pickteam = TCPickteam.objects.get(main_user = request.user)
                try:
                    retailer_name = data_js[0]['retailer_name']
                except:
                    return HttpResponse('retailer not found')

            creator = OrderCreator()
            sender = KakaoNotifySender()

            result = creator.create_orders_from_js(orders_js, request.user.username, retailer_name, pickteam.id)
            notifies = creator.notifies

            for ws_name in notifies:
                notify_id = notifies[ws_name]['notify_id']
                sender.set_msg(retailer_name=retailer_name, ws_name=ws_name, notify_id=notify_id)
                phones = ['010-8895-8454']

                ws_phone = notifies[ws_name]['phone']
                if ws_phone not in phones:
                    phones.append(ws_phone)

                for phone in phones:
                    sender.send_kakao_msg(phone)

                sender.clear()

            return HttpResponse("Ok")

@require_login()
@require_http_methods(['GET', 'POST'])
def modal_view(request):

    if request.method == "POST":

        # validate uploaded excel file before showing to modal view

        file = request.FILES['excel_file']

        validator = OrderExcelValidator()
        validator.set_file(file)
        success, msg = validator.validate()

        if not success:
            return render(request, 'app/excel_modal.html', context={'orders': None, 'retailer_name':None, 'msg':msg})

        orders, success, msg = validator.extract()

        retailer_name = ""
        is_retailer = common.check_group(request.user, 'retailer_group')

        if is_retailer:
            retailer_name = TCRetailer.objects.get(main_user=request.user).org_name
        else:
            retailer_name = request.POST['retailer_name']

        if success:
            return render(request, 'app/excel_modal.html', context={'orders': orders, 'retailer_name': retailer_name, 'msg':None})
        else:
            return render(request, 'app/excel_modal.html', context={'orders': None, 'retailer_name':None, 'msg':msg})

