from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(['POST'])
def bulk_orders(request):
    context = {}
    template = loader.get_template('app/form_upload.html')
    return HttpResponse(template.render(context,request))