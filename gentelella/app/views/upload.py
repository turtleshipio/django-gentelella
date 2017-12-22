from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from app.forms import DocumentForm
from app.decorators import require_token
from app import utils
from app.excel import UploadManager
from app.models import  Orders

from django.db import transaction
from app.kakao import KakaoSender
import json

import io
import xlrd


@require_token()
@require_http_methods(['GET', 'POST'])
def bulk_orders(request):

    if 'msg' in request.session:
        request.session['msg']= None
        request.session.modified = True

    token = request.session['token']
    decoded_token = utils.decode_token(token)

    context = utils.get_context_from_token(utils.decode_token(token))
    retail_user = utils.get_retail_user_from_token(decoded_token)

    if request.method == "GET":

        return render(request, 'app/form_upload.html', context=context)

    if request.method == "POST":

        if request.is_ajax():

            orders_js = json.loads(request.body.decode('utf-8'))
            notifies = {}
            orders = []

            for order_js in orders_js:

                ws_name = order_js['ws_name']

                if ws_name in notifies:
                    notify_id = notifies[ws_name]
                else:
                    notifies[ws_name] = utils.get_uuid(20)
                    notify_id = notifies[ws_name]

                order = Orders(
                    username=retail_user['username'],
                    retailer_id=retail_user['retailer_id'],
                    sizencolor=order_js['sizencolor'],
                    ws_phone=order_js['ws_phone'],
                    ws_name=ws_name,
                    product_name=order_js['product_name'],
                    building=order_js['building'],
                    floor=order_js['floor'],
                    location=order_js['location'],
                    count=order_js['count'],
                    price=order_js['price'],
                    is_deleted="false",
                    status="onwait",
                    notify_id=notify_id
                )

                orders.append(order)

            Orders.objects.bulk_create(orders)

            return HttpResponse("Ok")


        #request.session['msg'] = None
        #transaction.set_autocommit(False)
        #file = request.FILES['excel_file']

        #   manager = UploadManager()
        #manager.set_file(file)
        #manager.set_retail_user(retail_user)


        #success, msg = manager.validate()
        #sender = KakaoSender()
        #print("??????????????????????????")
        #print(sender)

        #msg = "소매점 션샤인에서 주문을 발송했습니다. 링크(goo.gl/1i2YrP)를 클릭하시면 주문내역을 확인하실 수 있습니다. 오늘도 좋은하루 보내세요~~ ^^"


        #response = sender.send_sms(msg, "01068680805")
        #response = sender.send_sms(msg, "01088958454")#염승헌
        #response = sender.send_sms(msg, "01036678070")#김병수
        #response = sender.send_sms(msg, "01085047804")#김태은

        #if not success:
        #    request.session['msg'] = msg
        #    return redirect('/upload_bulk/')

            #fails, msg = manager.insert_db()
        #manager.notify_orders()
        #transaction.commit()

        #sender = KakaoSender()
        #print("??????????????????????????")
        #response = sender.send_sms("test", "01088958454")


        #if fails > 0:
        #    request.session['msg'] = "{count}개 실패. {msg}".format(count=str(fails), msg=msg)
        #    return redirect('/upload_bulk')

        #return redirect('/order_list/')

@require_token()
@require_http_methods(['GET', 'POST'])
def modal_view(request):
    if request.method == "POST":

        file = request.FILES['excel_file']
        manager = UploadManager()
        manager.set_file(file)
        manager.validate()

        orders, success, msg = manager.extract()

        if success:
            return render(request, 'app/excel_modal.html', context={'orders': orders})
        else:
            return redirect('/upload_bulk')


