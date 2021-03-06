from django.views.generic.edit import ModelFormMixin
from django.views.generic.list import ListView
from django.db import IntegrityError
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from app.models import *
from app.forms.ws_form import CreateWsForm
from app.decorators import can_manage_ws, ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import  login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect
import json
from app.common import *
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from app.excel import BulkAddWsManager
from datetime import datetime

@login_required()
@ajax_required
def wsbytcorg(request):
    print("!!!!!")
    print("!!!!!")
    org = TCOrg.objects.get(main_user=request.user)
    print(org)
    ws_list = WsByTCGroup.objects.filter(org=org).exclude(is_deleted=True).order_by('-updated_time').values("updated_time", "ws_name", "building", "floor", "location", "col" )

    for ws in ws_list:
        ws['updated_time'] =ws['updated_time'].strftime('%Y-%m-%d')
        #ws['updated_time'] =datetime.strptime(str(ws['updated_time']), "%Y-%m-%d")

    print("!!!!!")
    print("!!!!!")
    print("!!!!!")
    print(len(ws_list))
    print("!!!!!")
    print("!!!!!")
    print("!!!!!")
    return JsonResponse(list(ws_list), safe=False)

@login_required()
@ajax_required
def search_ws(request):

    ws_name = request.POST['search_ws']
    ws_list = []

    try:
        group = TCGroup.objects.filter(main_user=request.user)[0]
        ws_list = WsByTCGroup.objects.filter(group=group).exclude(is_deleted=True).values("ws_name", "building", "location", "floor", "col", "ws_phone")

        data = {'ws_list': ws_list}
        return JsonResponse(data)

    except Exception as e:
        data = {'ws_list': []}
        return JsonResponse(data)

@login_required()
@require_http_methods(["POST"])
def bulk_add_ws(request):

    file = request.FILES['excel-file']

    if file is not None:
        try:
            manager = BulkAddWsManager(request.user)
            manager.set_file(file)
            manager.extract()

            response = HttpResponse()
            return response

        except Exception as e:
            response = HttpResponse()
            response.status_code= 500
            return response

    response = HttpResponse()
    response.status_code = 200
    return redirect('/manage_ws')



@require_http_methods(["PUT"])
def edit_wsbyuser(request):

    data_js = json.loads(request.body.decode('utf-8'))[0]
    ws_name = data_js['ws_name']
    building = data_js['building']
    floor = data_js['floor']
    location = data_js['location']
    col = data_js['col']
    ws_phone = data_js['ws_phone']

    try:
        group = TCGroup.objects.filter(main_user=request.user)[0]
        wsbygroup = get_object_or_404(WsByTCGroup, group=group, ws_name=ws_name, is_deleted=False)
        wsbygroup.building = building
        wsbygroup.floor = floor
        wsbygroup.location = location
        wsbygroup.ws_phone = ws_phone
        wsbygroup.col = col
        wsbygroup.save()
        return HttpResponse("ok")
    except Exception as e:
        response = HttpResponse(e)
        response.status_code = 500
        return response

@ajax_required
@login_required()
@require_http_methods(["PUT"])
def delete_wsbygroup(request):
    user = request.user
    data_js = json.loads(request.body.decode('utf-8'))[0]
    wsbyuser_id = data_js['id']

    try:
        group = TCGroup.objects.filter(main_user=user)[0]
        WsByTCGroup.objects.filter(group=group, id=wsbyuser_id).exclude(is_deleted=True).update(is_deleted=True)
        return HttpResponse("ok")
    except Exception as e:
        response = HttpResponse(e)
        response.status_code = 500
        return response

@ajax_required
@login_required()
@require_http_methods(["POST"])
def floors_by_building(request):

    data_js = json.loads(request.body.decode('utf-8'))[0]
    building = data_js['building']

    try:
        floors = Wholesalers.objects.filter(building_name=building).values_list('floor', flat=True).distinct()
        floors = list(floors)
        data = {'floors': floors}
        return JsonResponse(data)
    except Exception as e:
        response = HttpResponse("error")
        response.status_code = 500
        return response


class WSFormMixinListView(ModelFormMixin, ListView):
    model = WsByTCGroup
    form = CreateWsForm
    fields = ()
    context_object_name = 'ws'
    template_name = "app/manage_ws.html"
    paginate_by = 10


    def get_context_data(self, *args, **kwargs):
        context = super(WSFormMixinListView, self).get_context_data(*args, **kwargs)
        print("!!!!")
        print("!!!!")
        print(self.request.user)
        print("!!!!")
        print("!!!!")
        org = TCOrg.objects.get(main_user=self.request.user)

        is_retailer = org.group.name == "retailer_group"
        is_pickteam = org.group.name == "pickteam_group"
        is_staff = org.group.name == "staff"

        buildings = Buildings.objects.values_list('building_name', flat=True).order_by('building_name')


        ws_bulk_add_formats = BulkAddWsFormat.objects.values_list('format', flat=True)
        ws_bulk_add_formats = ', '.join(ws_bulk_add_formats)

        data = {
            'ws_bulk_add_formats' : ws_bulk_add_formats,
            'buildings' : buildings,
        }

        context['data'] = data
        context['form'] = self.get_form()
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden

        data_js = json.loads(request.body.decode('utf-8'))[0]
        ws_name = data_js['ws_name']
        building= data_js['building']
        floor   = data_js['floor']
        location= data_js['location']
        col = data_js['col']
        ws_phone= data_js['ws_phone']

        try:
            org = TCOrg.objects.get(main_user=self.request.user)
            ws_bytcuser = WsByTCGroup.objects.create(ws_name=ws_name,col=col, building=building, floor=floor, location=location, ws_phone=ws_phone, org=org)
            msg = "도매가 성공적으로 추가 되었습니다."
            messages.success(request, msg)
        except IntegrityError:
            messages.error(request, '도매추가를 실패하였습니다.')
            return HttpResponse('error')

        return self.get(request, *args, **kwargs)
