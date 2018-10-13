from django.utils.dateparse import parse_date
from django.views.generic.list import ListView
from django.http import *
from app.models import *
from braces.views import LoginRequiredMixin
import json
from app.excel import OrderExcelValidator
from app.common import check_group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import  login_required
from django.views.decorators.http import require_http_methods
from app.decorators import ajax_required
from django.shortcuts import render, redirect
from app.kakao import  *
from django.template import RequestContext
import datetime
from app.views.parsers import *
from app import custom_db

@login_required()
@require_http_methods(['POST'])
def edit_order_format(request):
    data_js = json.loads(request.body.decode('utf-8'))[0]

    retailer_name = data_js['retailer_name']
    fmt_ws_name = data_js['fmt_ws_name']
    fmt_product_name = data_js['fmt_product_name']
    fmt_sizeNcolor= data_js['fmt_sizeNcolor']
    fmt_color= data_js['fmt_color']
    fmt_price= data_js['fmt_price']
    fmt_count= data_js['fmt_count']
    fmt_request = data_js['fmt_request']

    try:
        retailer = TCRetailer.objects.get(org_name=retailer_name)
        format = OrderFormats.objects.get(tcretailer=retailer)
        format = retailer.order_format

        format.fmt_ws_name = fmt_ws_name
        format.fmt_product_name = fmt_product_name
        format.fmt_sizencolor = fmt_sizeNcolor
        format.fmt_color = fmt_color
        format.fmt_price = fmt_price
        format.fmt_count = fmt_count
        format.fmt_request = fmt_request
        format.save()

        response = HttpResponse("ok")
        response.status_code = 200
        return response

    except Exception as e:
        response = HttpResponse("error")
        response.status_code = 500
        return response



@login_required()
@require_http_methods(['GET', 'POST'])
def bulk_orders(request):
    context= {
        'retailer_name' : None,
        'order' : None
    }

    retailer = request.user.groups.filter(name="retailer_group")

    if len(retailer) > 0:
        context['retailer_name'] = retailer[0].name

    if request.method == "GET":
        request.FILES['excel_file'] = None
        return render(request, 'app/upload_bulk_orders.html', context=context)

    if request.method == "POST":

        if request.is_ajax():

            data_js = json.loads(request.body.decode('utf-8'))
            orders_js = data_js[0]['orders']

            #group = TCGroup.objects.filter(main_user=request.user)[0]
            #is_pickteam = (group.type == "pickteam")
            org = TCOrg.objects.get(main_user=request.user)
            is_pickteam = org.group.name=="pickteam_group"

            if is_pickteam:
                pickteam = org
                try:
                    retailer_name = data_js[0]['retailer_name']
                except:
                    response = HttpResponse('retailer not found')
                    response.status_code = 500
                    return response

            else: # if retailer
                retailer = TCRetailer.objects.get(main_user=request.user)
                retailer_name = retailer.org_name
                pickteam = retailer.pickteam


            #date = datetime.datetime.today().strftime('%Y-%m-%d')
            #creator = OrderCreator(date)
            creator = OrderCreator()
            sender = KakaoNotifySender()

            success = creator.create_orders_from_js(request.user, orders_js, request.user.username, retailer_name, pickteam.id, org)



            if not success:
                response = HttpResponse("error")
                response.status_code=500
                return response

            notifies = creator.notifies

            send = False

            if send:
                for ws_name in notifies:
                    notify_id = notifies[ws_name]['notify_id']
                    sender.set_msg(retailer_name=retailer_name, ws_name=ws_name, notify_id=notify_id)
                    phones = ['01088958454']

                    ws_phone = notifies[ws_name]['phone']
                    if ws_phone not in phones:
                        phones.append(ws_phone)

                    for phone in phones:
                        sender.send_kakao_msg(phone)

                    sender.clear()

            return HttpResponse("Ok")


@login_required()
@require_http_methods(['POST'])
def modal_excel_parse_view(request):

    if request.method == "POST":

        # validate uploaded excel file before showing to modal view

        file = request.FILES['excel_file']

        org = TCOrg.objects.get(main_user=request.user)
        is_pickteam = org.group.name == "pickteam_group"
        pickteam = None

        if is_pickteam:
            retailer_name = request.POST['retailer_name']
            org = TCOrg.objects.get(org_name=retailer_name)
            retailer = TCRetailer.objects.select_related('org').get(org=org)
            pickteam = TCOrg.objects.get(main_user=request.user)
        else:
            retailer = TCRetailer.objects.get(main_user=request.user)
            retailer_name = retailer.org_name
            pickteam = TCOrg.objects.get(id=retailer.pickteam_id)
        order_format = retailer.order_format

        # get parser by each retailer from app.views.parsers
        parser = globals()[retailer.parser]
        print(parser)
        parser = parser(user=request.user, file=file, local=False)
        parser.preprocess()
        parser.inspect_header(order_format)
        orders, has_datetime, success, msg = parser.extract(pickteam)
        parser.clear()



        context = {}
        context['has_datetime'] = has_datetime
        context['orders'] = orders
        context['retailer_name'] = retailer_name
        context['msg'] = msg
        context['success'] = success
        context['datetime'] = ""
        if success:
            return render(request, 'app/excel_modal.html', context=context)
        else:
            request.FILES['excel_file'] = None
            return render(request, 'app/excel_modal.html', context=context)




@login_required()
@ajax_required
@require_http_methods(['GET'])
def formats_by_retailer(request):
    try:
        retailer_name = request.GET.get('retailer_name')
        org = TCOrg.objects.get(org_name=retailer_name)
        retailer = TCRetailer.objects.get(org=org)
        format = retailer.order_format
        format_dict = format.get_format_dict()

        return JsonResponse(format_dict)

    except Exception as e:
        print(e)
        response = JsonResponse(data={})
        response.status_code = 500
        return response

class ManageOrderListView (LoginRequiredMixin, ListView):
    model = OrderGroup
    context_object_name = 'order_groups'
    template_name = "app/manage_orders1.html"
    login_url = '/'
    paginate_by = 20

    is_pickteam = True
    retailer = None
    pickteam = None
    orders = None
    order_groups = None

    org = None

    def get_queryset(self):

        self.org = TCOrg.objects.get(main_user=self.request.user)
        if self.is_pickteam:
            order_group = OrderGroup(self.org.id)
            self.order_groups = order_group.get_orders_by_pickteam()
        else:
            if self.is_retailer:
                self.retailer = TCRetailer.objects.get(main_user=self.request.user)
                self.orders = Order.objects.exclude(is_deleted=True).filter(retailer=self.retailer).values('ws_name', 'created_time', 'count', 'price', 'status', 'read').order_by('-created_time')
                order_group = OrderGroup(retailer_name=self.retailer.retailer_name)
                self.order_groups = order_group.get_orders_by_retailer()
        return self.order_groups


    def get_context_data(self, *args, **kwargs):
        context = super(ManageOrderListView, self).get_context_data(*args, **kwargs)
        self.org = TCOrg.objects.get(main_user=self.request.user)
        self.is_pickteam = self.org.group.name == "pickteam_group"
        self.is_retailer = self.org.group.name == "retailer_group"
        self.is_staff = self.org.group.name == "staff"

        retailers = None
        format = None
        format_str = None

        if self.is_pickteam:
            retailers = TCRetailer.objects.select_related('pickteam').filter(pickteam=self.org)
        else:
            if self.is_retailer:
                format = self.retailer.order_format
                format_str = format.get_format_str()

        paginator = Paginator(self.order_groups, self.paginate_by)
        page = self.request.GET.get('page')


        try:
            paged_orders = paginator.page(page)
        except PageNotAnInteger:
            paged_orders = paginator.page(1)
        except EmptyPage:
            paged_orders = paginator.page(paginator.num_pages)

        if self.is_pickteam:
            context['retailers'] = retailers

        context['is_pickteam'] = self.is_pickteam
        context['is_retailer'] = self.is_retailer
        context['is_staff'] = self.is_staff
        context['format'] = format
        context['format_str'] = format_str
        context['retailer_name'] = self.retailer.org_name if self.retailer else None
        context['orders'] = paged_orders if paged_orders else None
        context['num_pages'] = paginator.num_pages
        context['order'] = None

        return context



    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden
        if not request.is_ajax():
            return HttpResponseBadRequest

        data_js = json.loads(request.body.decode('utf-8'))[0]

        retailer_name = data_js['retailer_name']
        fmt_ws_name = data_js['fmt_ws_name']
        fmt_product_name = data_js['fmt_product_name']
        fmt_sizencolor= data_js['fmt_sizencolor']
        fmt_color= data_js['fmt_color']
        fmt_price= data_js['fmt_price']
        fmt_count= data_js['fmt_count']
        fmt_request = data_js['fmt_request']

        try:
            pickteam = TCPickteam.objects.get(main_user=self.request.user)
            retailer = TCRetailer.objects.get(pickteam_id=pickteam.id, org_name=retailer_name)
            format = retailer.order_format

            format.fmt_ws_name = fmt_ws_name
            format.fmt_product_name = fmt_product_name
            format.fmt_sizencolor = fmt_sizencolor
            format.fmt_color = fmt_color
            format.fmt_price = fmt_price
            format.fmt_count = fmt_count
            format.fmt_request = fmt_request
            format.save()
            response = HttpResponse()
            response.status_code= 200
            return response
        except Exception as e:
            response = HttpResponse()
            response.status_code=500
            return response


