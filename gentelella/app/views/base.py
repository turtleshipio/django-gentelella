from django.template import loader
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from passlib.apps import custom_app_context as pwd_context

from app.models import *

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from app.forms import *
from app.backend import RetailUserBackend
from app import utils
from app.decorators import require_token
from app import pickup_utils
import json
from app.views.auth.signup import create_turtlechain_user
from app.views.auth.login import retail_login, pickup_login
from django.template import Context

from django.contrib import auth

@require_token()
def home(request):

    try:
        token = request.session['token']
        token = utils.decode_token(token)
        context = utils.get_context_from_token(token)
        context['home'] = None
        context['content'] = None
        user = utils.get_user_from_token(token)
        context['t_user'] = user


        if Permissions.objects.filter(org_id=user.org_id, policy_name="wholesale").exists():
            context['ws_perm'] = True
        else:
            context['ws_perm'] = False


        context['login_error'] = None
        context['signup_error'] = None
        return render(request, 'app/index.html', context=context)
    except KeyError:
        return redirect('/')


def logout(request):

    try:
        request.session.flush()
        request.session.modified = True
        return redirect('/')
    except:
        return redirect('/')

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
    return render(request, 'app/form.html')


@require_http_methods(['GET', 'POST'])
def login(request):
    context = {}
    context['login_error'] = None
    context['signup_error'] = None

    if request.method == "GET":
        request.session.flush()
        request.session.modified = True
        return render(request, 'app/login.html', context=context)

    if request.method == "POST":

        context = {}
        success = False
        username = request.POST['username']
        password = request.POST['password']
        acc_type = request.POST['account-type']

        user = auth.authenticate(request=request, username=username, password=password)

        print("***")
        if user is not None:
            auth.login(request, user)

            return render(request, 'app/index.html', context=context)
        
        else:
            return redirect('/')
            return None
            
        """
        if acc_type == "retail":
            context, success = retail_login(request, username, password)

        if acc_type == "pickup":
            context, success = pickup_login(request, username, password)

        if success:
            return render(request, 'app/index.html', context=context)
        else:
            request.session.flush()
            request.session.modified = True
            context = {}
            context['login_error'] = True
            context['signup_error'] = True
            return render(request,'app/login.html', context=context)

        """ 
@require_http_methods(['GET', 'POST'])
def signup(request):
    context = {}
    context['styles'] = None

    if request.method == "GET":

        styles = StoreSyles.objects.values_list('style_en', 'style_kr')
        context['styles'] = styles
        return render(request, 'app/signup-form.html', context=context)

    if request.method == "POST":
        print("????")
        context['login_error'] = ""
        context['signup_error'] = ""
        context['content'] = ""
        context['ws_perm'] = False

        if 'signup-cancel' in request.POST:
            print("something wrong")
            return redirect('/home')

        data_js = json.loads(request.body.decode('utf-8'))

        success, t_user, token = create_turtlechain_user(data_js)

        print("???RESULT!!!!!!")
        print(success)

        if success:
            
            context['t_user'] = t_user
            request.session['token'] = token
            org_id = t_user.org_id
            if Permissions.objects.filter(org_id=org_id, policy_name="wholesale").exists():
                context['ws_perm'] = True
            else:
                context['ws_perm'] = False
                
            print("??????")
            print("what?s in context?")
            print(context)
            
            return HttpResponseRedirect(reverse('home'))
            #return render(request, 'app/index.html', context=context)
        
        else:
            return render(request, 'app/signup-form.html', context)
    

@require_token()
@require_http_methods(["POST"])
def delete_order(request):

    if request.method == 'POST':
        form = OrderListDeleteForm(request.POST)

        if form.is_valid():

            order_id = form.cleaned_data['order_id']
            Orders.objects.filter(order_id=order_id).update(is_deleted='true')

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
                Orders.objects.filter(pk__in=choices[choice]).update(status=choice)

            return render(request, 'app/alert.html', context=context)

    return redirect('/')
