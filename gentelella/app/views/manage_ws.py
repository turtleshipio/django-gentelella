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

from app.excel import BulkAddWsManager

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
        return JsonResponse(data);
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
        is_retailer = check_group(self.request.user, 'retailer_group')
        is_pickteam = check_group(self.request.user, 'pickteam_group')
        is_staff = check_group(self.request.user, 'staff')

        if is_pickteam or is_staff:
            group = TCGroup.objects.get(main_user=self.request.user, type="pickteam")
        else:
            group = TCGroup.objects.get(main_user=self.request.user, type="retailer")

        buildings = Buildings.objects.values_list('building_name', flat=True).order_by('building_name')

        ws_list = WsByTCGroup.objects.filter(group=group).exclude(is_deleted=True).order_by('-updated_time')
        paginator = Paginator(ws_list, self.paginate_by)

        page = self.request.GET.get('page')
        try:
            ws = paginator.page(page)
        except PageNotAnInteger:
            ws = paginator.page(1)
        except EmptyPage:
            ws = paginator.page(paginator.num_pages)

        ws_bulk_add_formats = BulkAddWsFormat.objects.values_list('format', flat=True)
        ws_bulk_add_formats = ', '.join(ws_bulk_add_formats)

        data = {
            'ws_bulk_add_formats' : ws_bulk_add_formats,
            'buildings' : buildings,
            'ws_list' : ws_list,
        }

        context['data'] = data
        context['num_pages'] = paginator.num_pages
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
            group = TCGroup.objects.filter(main_user=request.user)[0]
            ws_bytcuser = WsByTCGroup.objects.create(ws_name=ws_name,col=col, building=building, floor=floor, location=location, ws_phone=ws_phone, group=group)
            msg = "도매가 성공적으로 추가 되었습니다."
            messages.success(request, msg)
        except IntegrityError:
            messages.error(request, '도매추가를 실패하였습니다.')
            return HttpResponse('error')

        return self.get(request, *args, **kwargs)
