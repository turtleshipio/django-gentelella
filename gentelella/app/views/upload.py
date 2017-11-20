from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from app.forms.document import  DocumentForm

@require_http_methods(['GET','POST'])
def bulk_orders(request):
    context = {}
    template = loader.get_template('app/form_upload.html')
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['docfile']
            template = loader.get_template('app/index.html')


    return HttpResponse(template.render(context,request))