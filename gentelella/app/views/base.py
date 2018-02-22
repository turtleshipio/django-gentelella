from django.template import loader
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from passlib.apps import custom_app_context as pwd_context

from app.models import *
from django.shortcuts import redirect, render
from app.forms import *
from app.backend import RetailUserBackend
#from passlib.hash import sha256_crypt
from app import utils
from app.decorators import require_token
from app import pickup_utils
import json

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


def signup_check(request):

    data_js = json.loads(request.body.decode('utf-8'))
    username = data_js['username']
    payload = {'msg': None}
    try:
        exists = RetailUser.objects.filter(username=username).exists()

        if exists:
            payload['msg'] = 'error'
        else:
            payload['msg'] = 'ok'

        return HttpResponse(json.dumps(payload))

    except RetailUser.DoesNotExist:
        return HttpResponse("error")
    return HttpResponse(str(e))



def check_business_number(request):
    print("******************")
    print("******************")
    print("******************")
    print("******************")
    print("******************")
    print("******************")

    data_js = json.loads(request.body.decode('utf-8'))
    business_number = data_js['business_number']
    payload = {'msg': None}
    try:
        exists = Retailer.objects.filter(business_number=business_number).exists()

        if exists:
            payload['msg'] = 'error'
        else:
            payload['msg'] = 'ok'

        return HttpResponse(json.dumps(payload))

    except Retailer.DoesNotExist:
        return HttpResponse("error")



def logout(request):

    try:
        request.session.flush()
        request.session.modified = True
        return redirect('/')
    except:
        return redirect('/')


def notify(request):
    return render(request, 'app/notify.html')

def notify_success(request):

    if request.method == "POST":
        notify_id = request.POST.get("notify_id", "")

        context = {'notify_id': notify_id}

        return render(request, 'app/alert.html', context=context)


def temp(request):

    return render(request, 'app/form.html')


def retail_login(request, username, password):
    context = {}
    context['login_error'] = ""
    context['signup_error'] = ""
    context['content'] = ""
    context['ws_perm'] = False

    try:
        retail_user = RetailUser.objects.exclude(retailer_id=-1).get(username=username)
        pwd_valid = pwd_context.verify(password, retail_user.password)

        user = TurtlechainUser(retail_user)
        org_id = user.org_id
        context['t_user'] = user

        if pwd_valid:
            token = utils.issue_token(username, retail_user.phone, retail_user.retailer_id, retail_user.retailer_name,
                                      retail_user.name)
            request.session['token'] = token
            if Permissions.objects.filter(org_id=org_id, policy_name="wholesale").exists():
                context['ws_perm'] = True
            return context, True

    except RetailUser.DoesNotExist:
        context['login_error'] = True
        return context, False
    except ValueError:
        context['login_error'] = True
        return context, False

    return context, False



def pickup_login(request, username, password):

    context = {}
    context['login_error'] = ""
    context['signup_error'] = ""
    context['content'] = ""
    context['ws_perm'] = False

    try:
        pickup_user = PickupUser.objects.exclude(pickup_user_id=-1).get(username=username)
        pwd_valid = pwd_context.verify(password, pickup_user.password)

        user = TurtlechainUser(pickup_user)
        org_id = user.org_id
        context['t_user'] = user


        if pwd_valid:
            token = pickup_utils.issue_token(username, pickup_user.phone, pickup_user.pickup_user_id, pickup_user.name, pickup_user.pickteam_id)
            request.session['token'] = token

            if Permissions.objects.filter(org_id=org_id, policy_name="wholesale").exists():
                context['ws_perm'] = True
            return context, True

    except PickupUser.DoesNotExist:
        context['login_error'] = True
        return context, False
    except ValueError:
        context['login_error'] = True
        return context, False

    print(context['ws_perm'])
    return context, False





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

        context = None
        success = False
        username = request.POST['username']
        password = request.POST['password']
        acc_type = request.POST['account-type']



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



@require_http_methods(['GET', 'POST'])
def signup(request):
    context = {}

    if request.method == "GET":

        styles = StoreSyles.objects.values_list('style_en', 'style_kr')
        context['styles'] = styles
        return render(request, 'app/signup-form.html', context=context)

    if request.method == "POST":
        try:

            form = SignUpForm(request.POST)

            if form.is_valid():

                username = form.cleaned_data['username']
                name = form.cleaned_data['name']
                phone = form.cleaned_data['phone']
                password = form.cleaned_data['password']

                enc_password = pwd_context.encrypt(password)
                retail_user = \
                    RetailUser(username=username, name=name,
                               password=enc_password, phone=phone, retailer_id=-1)
                retail_user.save()

                if retail_user is None:
                    retail_user = {'username': 'test'}

                context = {'retail_user': retail_user}

                return render(request, template_name='app/index.html', context=context)

            else:
                context['signup_error'] = True
                return render(request, 'app/login.html', context=context)
        except KeyError:
            request.session.flush()
            request.session.modified = True
            context['signup_error'] = True
            return render(request, 'app/login.html', context=context)
        except:
            request.session.flush()
            request.session.modified = True
            context['signup_error'] = True
            return render(request, 'app/login.html', context=context)


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)

    return HttpResponse(template.render(context, request))


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
