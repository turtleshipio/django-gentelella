from django.template import loader
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from app.models import Orders, RetailUser
from django.shortcuts import redirect, render
from app.forms import *
from app.backend import RetailUserBackend
from passlib.hash import sha256_crypt


def index(request):
    context = {}
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render(context, request))


@require_http_methods(['GET', 'POST'])
def login(request):

    context = {}
    if request.method == "GET":
        return render(request, 'app/login.html')
    if request.method == "POST":

        try:
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                try:
                    retail_user = RetailUser.objects.get(username=username)
                except RetailUser.DoesNotExist:
                    return redirect('/')

                pwd_valid = sha256_crypt.verify(password, retail_user.password)

                if pwd_valid:
                    context['retail_user'] = retail_user
        except KeyError:
            return redirect("/")
        except BaseException:
            return redirect("/")

        return render(request, 'app/index.html', context=context)


@require_http_methods(['POST'])
def signup(request):

    try:

        form = SignUpForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            print("*****************************************")
            print("*****************************************")
            print("*****************************************")
            #username = request.POST['username']
            #name = request.POST['name']
            #phone = request.POST['phone']
            #password = request.POST['password']

            print("*****************************************")
            print("*****************************************")
            print("*****************************************")
            print("*****************************************")



            enc_password = sha256_crypt.encrypt(password)
            retail_user = RetailUser(username=username, name=name, password=enc_password, phone=phone)
            retail_user.save()
            print("*****************************************")
            print("*****************************************")
            print("*****************************************")
            print("*****************************************")
            print(retail_user)
            if retail_user is None:
                retail_user = {'username' : 'test'}
            print("*****************************************")
            print("*****************************************")
            print("*****************************************")
            print("*****************************************")
            print("*****************************************")
            context = {'retail_user':retail_user}
            #retail_user = RetailUser.objects.get(username=username)
            return render(request, template_name='app/index.html', context=context)
        else:
            print("?????????????????????????????")
            print("?????????????????????????????")
            print("?????????????????????????????")
            return redirect('/')
    except KeyError:
        return redirect('/')
    except BaseException:
        return redirect('/')


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))


@require_http_methods(["POST"])
def delete(request):

    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]

    if request.method == 'POST':
        form = OrderListDeleteForm(request.POST)

        if form.is_valid():

            order_id = form.cleaned_data['order_id']
            Orders.objects.filter(order_id=order_id).update(is_deleted='true')

            return redirect('/order_list/')

    return render(request, 'app/index.html')

