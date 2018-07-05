from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from app.excel import OrderExcelValidator
from app.models import *
from app import common
from app.kakao import OrderCreator, KakaoNotifySender
import json
from django.contrib.auth.decorators import  login_required

@login_required()
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
        request.FILES['excel_file'] = None
        return render(request, 'app/upload_bulk_orders.html', context=context)

    if request.method == "POST":

        if request.is_ajax():

            data_js = json.loads(request.body.decode('utf-8'))
            orders_js = data_js[0]['orders']

            is_pickteam = common.check_group(request.user, 'pickteam_group')

            if is_pickteam:
                pickteam = TCPickteam.objects.get(main_user = request.user)
                try:
                    retailer_name = data_js[0]['retailer_name']
                except:
                    return HttpResponse('retailer not found')

            else: # if pickteam
                retailer = TCRetailer.objects.get(main_user=request.user)
                retailer_name = retailer.org_name

                group = request.user.groups.get(name='retailer_group')
                pickteam = retailer.pickteam # technically should be foreign key instead of n:n. Just for now.

            creator = OrderCreator()
            sender = KakaoNotifySender()

            success = creator.create_orders_from_js(request.user, orders_js, request.user.username, retailer_name, pickteam.id)

            if not success:
                response = HttpResponse("error")
                response.status_code=500
                return response

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

@login_required()
@require_http_methods(['GET', 'POST'])
def modal_view(request):

    if request.method == "POST":

        # validate uploaded excel file before showing to modal view

        file = request.FILES['excel_file']

        validator = OrderExcelValidator(request.user)
        validator.set_file(file)

        is_pickteam = common.check_group(request.user, 'pickteam_group')

        if is_pickteam:
            retailer_name = request.POST['retailer_name']
            retailer = TCRetailer.objects.get(org_name=retailer_name)

        else:
            retailer = TCRetailer.objects.get(main_user=request.user)
            retailer_name = retailer.org_name

        order_format = retailer.order_format
        success, msg = validator.validate(order_format)

        if not success:
            return render(request, 'app/excel_modal.html', context={'orders': None, 'retailer_name':None, 'msg':msg})

        orders, success, msg = validator.extract()


        if success:
            return render(request, 'app/excel_modal.html', context={'orders': orders, 'retailer_name': retailer.org_name, 'msg':None})
        else:
            request.FILES['excel_file'] = None
            return render(request, 'app/excel_modal.html', context={'orders': None, 'retailer_name':None, 'msg':msg})

