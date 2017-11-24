from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from app.forms import DocumentForm
from app.decorators import require_token
from app import utils
from app.excel import UploadManager
from django.db import transaction
import io
import xlrd


@require_token()
@require_http_methods(['GET', 'POST'])
def bulk_orders(request):

    #if 'msg' in request.session:
    #    request.session['msg']= None
    #    request.session.modified = True

    token = request.session['token']
    decoded_token = utils.decode_token(token)
    context = utils.get_context_from_token(utils.decode_token(token))
    retail_user = utils.get_retail_user_from_token(decoded_token)

    if request.method == "GET":
        return render(request, 'app/form_upload.html', context=context)

    if request.method == "POST":
        transaction.set_autocommit(False)
        file = request.FILES['excel_file']

        manager = UploadManager()
        manager.set_file(file)
        manager.set_retail_user(retail_user)
        success, msg = manager.validate()

        if not success:
            request.session['msg'] = msg
            return redirect('/upload_bulk/')

        fails, msg = manager.insert_db()
        transaction.commit()

        if fails > 0:
            request.session['msg'] = "{count}개 실패. {msg}".format(count=str(fails), msg=msg)
            return redirect('/upload_bulk')

        return redirect('/order_list/')


