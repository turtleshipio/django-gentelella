from django.template import loader
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from app.models import *
from django.shortcuts import redirect, render
from app.forms import *
from app.backend import RetailUserBackend
from passlib.hash import sha256_crypt
from app import utils
from app.decorators import require_token
from app import pickup
@require_token()
def home(request):

    try:
        token = request.session['token']
        context = utils.get_context_from_token(utils.decode_token(token))
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


def notify(request):
    return render(request, 'app/notify.html')

def notify_success(request):

    if request.method == "POST":
        notify_id = request.POST.get("notify_id", "")

        context = {'notify_id': notify_id}

        return render(request, 'app/alert.html', context=context)


def temp(request):

    return render(request, 'app/alert.html')

def retail_login(request, username, password):

    context = {}

    try:
        retail_user = RetailUser.objects.exclude(retailer_id=-1).get(username=username)
        pwd_valid = sha256_crypt.verify(password, retail_user.password)
        context['retail_user'] = retail_user
        if pwd_valid:
            token = utils.issue_token(username, retail_user.phone, retail_user.retailer_id, retail_user.retailer_name,
                                      retail_user.name)
            request.session['token'] = token
            return redirect('home')

    except RetailUser.DoesNotExist:
        context['login_error'] = True
        return render(request, 'app/login.html', context=context)
    except ValueError:
        context['login_error'] = True
        return render(request, 'app/login.html', context=context)


def pickup_login(request, username, password):

    context = {}
    print("&&&&&&&&&&&&&&&&&&&")
    print("&&&&&&&&&&&&&&&&&&&")
    try:
        pickup_user = PickupUser.objects.exclude(pickup_user_id=-1).get(username=username)
        pwd_valid = sha256_crypt.verify(password, pickup_user.password)
        print("&&&&&&&&&&&&&&&&&&&")
        print(pwd_valid)
        print("&&&&&&&&&&&&&&&&&&&")
        user = TurtlechainUser(pickup_user)
        user = {'name' : "hi"}
        context['t_user'] = user
        print("&&&&&&&&&&&&&&&&&&&")
        print("&&&&&&&&&&&&&&&&&&&")
        print("&&&&&&&&&&&&&&&&&&&")
        print(user['name'])
        print("&&&&&&&&&&&&&&&&&&&")
        print("&&&&&&&&&&&&&&&&&&&")
        print("&&&&&&&&&&&&&&&&&&&")
        print("&&&&&&&&&&&&&&&&&&&")
        print("&&&&&&&&&&&&&&&&&&&")
        print("&&&&&&&&&&&&&&&&&&&")

        if pwd_valid:
            token = pickup.utils.issue_token(username,
                                             pickup_user.phone,)
            request.session['token'] = token
            return context

    except PickupUser.DoesNotExist:
        context['login_error'] = True
        return context
    except ValueError:
        context['login_error'] = True
        return context

    return context





@require_http_methods(['GET', 'POST'])
def login(request):

    if request.method == "GET":
        return render(request, 'app/login.html')
    if request.method == "POST":

        context = None
        username = request.POST['username']
        password = request.POST['password']
        acc_type = request.POST['account-type']

        if acc_type == "retail":
            return retail_login(request, username, password)

        if acc_type == "pickup":
            context =  pickup_login(request, username, password)

        return render(request, 'app/index.html', context=context)




@require_http_methods(['POST'])
def signup(request):
    context = {}
    try:

        form = SignUpForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']

            enc_password = sha256_crypt.encrypt(password)
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
            print("&&&&&&&&&&&&&&&&&&&&&&")
            print("&&&&&&&&&&&&&&&&&&&&&&")
            print(context)
            print("&&&&&&&&&&&&&&&&&&&&&&")
            print("&&&&&&&&&&&&&&&&&&&&&&")
            print("&&&&&&&&&&&&&&&&&&&&&&")
            print("&&&&&&&&&&&&&&&&&&&&&&")
            print("&&&&&&&&&&&&&&&&&&&&&&")
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
