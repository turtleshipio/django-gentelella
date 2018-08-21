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
<<<<<<< HEAD
from django.template import RequestContext
=======
import datetime
>>>>>>> 17d818d3569a9cbb7080ac982a67104c38fdb56c

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

            group = TCGroup.objects.filter(main_user=request.user)[0]
            is_pickteam = (group.type == "pickteam")

            if is_pickteam:
                pickteam = TCPickteam.objects.get(main_user = request.user)
                try:
                    retailer_name = data_js[0]['retailer_name']
                except:
                    response = HttpResponse('retailer not found')
                    response.status_code = 500
                    return response

            else: # if pickteam
                retailer = TCRetailer.objects.get(main_user=request.user)
                retailer_name = retailer.org_name
                pickteam = retailer.pickteam


<<<<<<< HEAD
            #date = datetime.datetime.today().strftime('%Y-%m-%d')
            #creator = OrderCreator(date)
            creator = OrderCreator()
=======
            date = datetime.datetime.strptime("2018-08-03", "%Y-%m-%d")

            creator = OrderCreator(date)
>>>>>>> 17d818d3569a9cbb7080ac982a67104c38fdb56c
            sender = KakaoNotifySender()

            success = creator.create_orders_from_js(request.user, orders_js, request.user.username, retailer_name, pickteam.id, group)

            if not success:
                response = HttpResponse("error")
                response.status_code=500
                return response
            """
            notifies = creator.notifies

            for ws_name in notifies:
                notify_id = notifies[ws_name]['notify_id']
                sender.set_msg(retailer_name=retailer_name, ws_name=ws_name, notify_id=notify_id)
                phones = []

                ws_phone = notifies[ws_name]['phone']
                if ws_phone not in phones:
                    phones.append(ws_phone)

                for phone in phones:
                    sender.send_kakao_msg(phone)

                sender.clear()

            """
            return HttpResponse("Ok")


@login_required()
@require_http_methods(['POST'])
def modal_view(request):

    if request.method == "POST":

        # validate uploaded excel file before showing to modal view

        file = request.FILES['excel_file']

        validator = OrderExcelValidator(request.user)
        validator.set_file(file)

        is_pickteam = check_group(request.user, 'pickteam_group')

        if is_pickteam:
            retailer_name = request.POST['retailer_name']
            retailer = TCRetailer.objects.get(org_name=retailer_name)

        else:
            retailer = TCRetailer.objects.get(main_user=request.user)
            retailer_name = retailer.org_name

        order_format = retailer.order_format
        success, msg = validator.validate(order_format)

        request
        if not success:
            return render(request, 'app/excel_modal.html', context={'orders': None, 'retailer_name':None, 'msg':msg})

        orders, has_datetime, success, msg = validator.extract()

        context = {}
        context['has_datetime'] = has_datetime
        context['orders'] = orders
        context['retailer_name'] = retailer_name
        context['msg'] = msg
        context['success'] = success

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
        retailer = TCRetailer.objects.get(org_name=retailer_name)
        format = retailer.order_format
        format_dict = format.get_format_dict()

        return JsonResponse(format_dict)

    except Exception as e:
        print(e)
        response = JsonResponse(data={})
        response.status_code = 500
        return response

class ManageOrderListView (LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = "app/manage_orders.html"
    login_url = '/'
    paginate_by = 20

    is_pickteam = True
    retailer = None
    pickteam = None
    orders = None

    def get_queryset(self):
        self.orders = []

        self.is_pickteam = check_group(self.request.user, 'pickteam_group')
        self.is_retailer = check_group(self.request.user, 'retailer_group')
        self.is_staff = check_group(self.request.user, 'is_staff')



        if self.is_pickteam:
            self.pickteam = TCPickteam.objects.get(main_user=self.request.user)
            self.orders = Order.objects.exclude(is_deleted=True).filter(pickteam=self.pickteam).values('ws_name', 'created_time', 'retailer_name', 'count', 'price', 'status', 'read').order_by('-created_time')
        else:
            if self.is_retailer:
                self.retailer = TCRetailer.objects.get(main_user=self.request.user)
                self.orders = Order.objects.exclude(is_deleted=True).filter(retailer=self.retailer).values('ws_name', 'created_time', 'count', 'price', 'status', 'read').order_by('-created_time')


        return self.orders


    def get_context_data(self, *args, **kwargs):
        context = super(ManageOrderListView, self).get_context_data(*args, **kwargs)

        self.is_pickteam = check_group(self.request.user, 'pickteam_group')
        self.is_retailer = check_group(self.request.user, 'retailer_group')
        self.is_staff = check_group(self.request.user, 'staff')

        retailers = None
        format = None
        format_str = None

        if self.is_pickteam:
            retailers = TCRetailer.objects.filter(pickteam=self.pickteam).values_list('org_name', flat=True)
        else:
            if self.is_retailer:
                format = self.retailer.order_format
                format_str = format.get_format_str()

        paginator = Paginator(self.orders, self.paginate_by)
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
            retailer = TCRetailer.objects.get(pickteam=pickteam, org_name=retailer_name)
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


