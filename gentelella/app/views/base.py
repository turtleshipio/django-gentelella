from django.views.decorators.http import require_http_methods
from app.common import check_group


from app.models import *

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render
import json
from app.views.auth.signup import create_turtlechain_user

from django.contrib import auth


@require_http_methods(['GET'])
def home(request):

    context = {}

    is_staff = check_group(request.user, 'staff')
    is_pickteam  = check_group(request.user, 'pickteam')
    is_retailer = check_group(request.user, 'retailer')

    print("!!!!!!!!!")
    print("!!!!!!!!!")
    print(is_staff)
    print("!!!!!!!!!")
    request.session['is_staff'] = is_staff
    request.session['is_pickteam'] = is_pickteam
    request.session['is_retailer'] = is_retailer

    context['content'] = None

    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'app/index.html', context=context)


def login(request):

    if request.user.is_authenticated():
        return redirect('/manage_orders')

    if request.method == "GET":

        return render(request, 'app/login.html')

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request=request, username=username, password=password)

        if user is not None:
            auth.login(request, user)

            is_staff = check_group(request.user, 'staff')
            is_pickteam  = check_group(request.user, 'pickteam_group')
            is_retailer = check_group(request.user, 'retailer_group')

            print("!!!!")
            print("!!!!")
            print(is_pickteam)
            print("!!!!")
            print("!!!!")
            print("!!!!")

            request.session['is_staff'] = is_staff
            request.session['is_pickteam'] = is_pickteam
            request.session['is_retailer'] = is_retailer

            return redirect('/home/')

        else:
            return redirect('/')

def logout(request):

    if request.user.is_active:
        auth.logout(request)

    return HttpResponseRedirect('/')



@require_http_methods(['GET'])
def notify(request):
    return render(request, 'app/notify.html')

@require_http_methods(['POST'])
def notify_success(request):

    notify_id = request.POST.get("notify_id", "")
    context = {'notify_id': notify_id}

    return render(request, 'app/alert.html', context=context)

@require_http_methods(['GET'])
def temp(request):
    return render(request, 'app/form_buttons.html')


@require_http_methods(['GET', 'POST'])
def signup(request):
    context = {}
    context['styles'] = None

    if request.method == "GET":

        styles = StoreSyles.objects.values_list('style_en', 'style_kr')
        context['styles'] = styles
        return render(request, 'app/signup-form.html', context=context)

    if request.method == "POST":
        context['login_error'] = ""
        context['signup_error'] = ""
        context['content'] = ""
        context['ws_perm'] = False

        if 'signup-cancel' in request.POST:
            return redirect('/home')

        data_js = json.loads(request.body.decode('utf-8'))

        success, user = create_turtlechain_user(data_js)


        if success:

            if user is not None:
                auth.login(request, user)
                return redirect('/home/')

            else:
                return redirect('/')
        else:
            redirect('/')
    

@require_http_methods(["POST"])
def delete_order(request):

    if request.method == 'POST':
        form = OrderListDeleteForm(request.POST)

        if form.is_valid():

            order_id = form.cleaned_data['order_id']
            Order.objects.filter(order_id=order_id).update(is_deleted='true')

            return redirect('/order_list/')

    return render(request, 'app/index.html')


@require_http_methods(["POST"])
def order_confirm(request):

    if request.method == 'POST':

            choice_list = request.POST.getlist('choice')
            notify_id = request.POST.get('notify_id')
            context = {'notify_id' : notify_id}

            choices = {}

            for choice in choice_list:
                c = choice.split('.')
                order_id = c[0]
                status = c[1]
                if status in choices:
                    choices[status].append(order_id)
                else:
                    choices[status] = [order_id]

            for choice in choices:
                Order.objects.filter(pk__in=choices[choice]).update(status=choice)

            return render(request, 'app/alert.html', context=context)

    return redirect('/')
