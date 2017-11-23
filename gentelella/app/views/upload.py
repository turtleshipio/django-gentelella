from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from app.forms import DocumentForm
from app.decorators import require_token
from app import utils


@require_token()
@require_http_methods(['GET', 'POST'])
def bulk_orders(request):

    token = request.session['token']
    context = utils.get_context_from_token(utils.decode_token(token))

    if request.method == "GET":
        return render(request, 'app/form_upload.html', context=context)

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['docfile']

            return redirect('/upload_bulk/')

