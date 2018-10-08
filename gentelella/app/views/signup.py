from django.http import HttpResponse
from django.shortcuts import  render, redirect
import json
from app.models import *
from django.contrib import auth
import pyotp
from app.kakao import KakaoNotifySender


def get_pyotp(request):
    print("????")
    print("????")
    print("????")
    print("????")
    print("????")
    print("????")

    otp = pyotp.TOTP("dsfldijaldi21o")

    sender = KakaoNotifySender()
    msg = sender.set_sms(str(otp))
    sender.send_sms(msg, "01088958454")

    return HttpResponse("ok")

def done(request):
    print("???")
    return render(request, 'app/signup/signup-pickteam-done.html')

def signup_pickteam(request):

    if request.method == "GET":
        context = {'sid' : request.session.session_key}
        print(request.session.session_key)
        return render(request, 'app/signup/signup-pickteam.html', context=context)

    if request.method == "POST":


        data_js = json.loads(request.body.decode('utf-8'))
        username = data_js['username']
        password = data_js['password']
        phone = data_js['phone']
        full_name = data_js['full_name']

        try:
            #user = TCUser.objects.create_user(username=username, password=password, full_name=full_name)
            #TCOrg.objects.create(org_name=full_name, main_user=user, group_id=3)
            temp = Temp.objects.create(username=username, password=password, full_name=full_name, phone=phone)
            print(data_js)
            return render(request, 'app/signup-pickteam-done.html')
        except Exception as e:
            print(str(e))
            return HttpResponse("ok")

