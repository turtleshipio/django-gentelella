from django.template import loader
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from app.forms import OrderListDeleteForm
from django.shortcuts import render
from app.models import Orders
from django.shortcuts import redirect

def index(request):
    context = {}
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render(context, request))


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
        print("**************************************")
        if form.is_valid():
            print("**************************************")
            print("**************************************")
            print("**************************************")
            order_id = form.cleaned_data['order_id']
            print(order_id)
            print("**************************************")
            print("**************************************")
            print("**************************************")
            order = Orders.objects.filter(order_id=order_id).update(is_deleted='true')

            return redirect('/order_list/')

    template = loader.get_template('app/index.html')

    return render(request, 'app/index.html', {'content': 'Hello'})