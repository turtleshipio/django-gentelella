from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from app.forms import DocumentForm
from app.decorators import require_token, require_login
from app import utils
from app.excel import UploadManager
from app.models import  Orders, RetailerPickteam

from django.db import transaction
from app.kakao import KakaoSender
import json

import io
import xlrd


@require_login()
@require_http_methods(['GET', 'POST'])
def bulk_orders(request):
    context= {}
    """
    if 'msg' in request.session:
        request.session['msg']= None
        request.session.modified = True

    token = request.session['token']
    decoded_token = utils.decode_token(token)
    context = utils.get_context_from_token(decoded_token)
    t_user = utils.get_user_from_token(decoded_token)
    context['t_user'] = t_user
    """

    retailer = request.user.groups.filter(name="retailer_group")

    if len(retailer) > 0:

        context['retailer_name'] = retailer[0].name

    #pickteam_id = t_user.pickteam_id


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

            notifies = {}
            orders = []

            for order_js in orders_js:

                ws_name = order_js['ws_name']

                if ws_name in notifies:
                    notify_id = notifies[ws_name]['notify_id']
                    count = order_js['count']
                    notifies[ws_name]['prd_count'] += int(count)
                else:
                    notify = {}
                    notify_id = utils.get_uuid(70)
                    notify['notify_id'] = notify_id
                    notify['prd_count'] = int(order_js['count'])
                    notify['prd1'] = order_js['product_name']
                    notify['phn'] = order_js['ws_phone']
                    notifies[ws_name] = notify

                username = t_user.username

                order = Orders(
                    username=username,
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
                    notify_id=notify_id,
                    pickteam_id=pickteam_id,
                        retailer_name=retailer_name,

                )


                orders.append(order)
            try:
                Orders.objects.bulk_create(orders)
            except Exception as e:
                print(str(e))
            finally:

                sender = KakaoSender()

                phones = ['01036678070']
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


        #request.session['msg'] = None
        #transaction.set_autocommit(False)
        #file = request.FILES['excel_file']

        #   manager = UploadManager()
        #manager.set_file(file)
        #manager.set_retail_user(retail_user)


        #success, msg = manager.validate()

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

        token = request.session['token']
        token = utils.get_decoded_token(token)

        retailer_name = ""
        if 'retailer_name' in request.POST:
            retailer_name = request.POST['retailer_name']
        if retailer_name == "":
            retailer_name = token['retailer_name']

        print(retailer_name)

        file = request.FILES['excel_file']


        manager = UploadManager()
        manager.set_file(file)
        manager.validate()

        orders, success, msg = manager.extract()
        print(msg)
        print("???????????????????????")
        if success:
            return render(request, 'app/excel_modal.html', context={'orders': orders, 'retailer_name': retailer_name, 'msg':None})
        else:
            return render(request, 'app/excel_modal.html', context={'orders': None, 'retailer_name':None, 'msg':msg})



