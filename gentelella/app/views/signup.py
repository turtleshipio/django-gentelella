from django.http import HttpResponse
from django.shortcuts import  render, redirect
import json
from app.models import *
from django.contrib import auth

def signup_pickteam(request):

    if request.method == "GET":
        return render(request, 'app/signup/signup-pickteam.html')

    if request.method == "POST":


        data_js = json.loads(request.body.decode('utf-8'))
        username = data_js['username']
        password = data_js['password']
        phone = data_js['phone']
        full_name = data_js['full_name']

        try:
            user = TCUser.objects.create_user(username=username, password=password, full_name=full_name)
            TCOrg.objects.create(org_name=full_name, main_user=user, group_id=3)

            if user is not None:
                auth.login(request, user)
                return redirect('/home/')
            else:
                return redirect("/")
        except Exception as e:
            print(str(e))
            return redirect("/")

