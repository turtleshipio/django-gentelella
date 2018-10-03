from django.conf.urls import url, include
from django.contrib import admin
from app.views.auth import checks
from app.views import base, upload
from app.views.order_list import OrderListView
from app.views.notify_list import NotifyListView
from app.views.manage_ws import WSFormMixinListView, delete_wsbygroup, floors_by_building, edit_wsbyuser, bulk_add_ws
from app.views.manage_retailers import TCRetailersListView
from app.views.manage_orders import ManageOrderListView, formats_by_retailer, modal_excel_parse_view, bulk_orders, edit_order_format
from app.views.super_stats import SuperStatsView
from app.views.signup import *

urlpatterns = [
    url(r'^super/', admin.site.urls),
    url(r'^$', base.login, name='login'),
    url(r'^login', base.login, name='login'),
    url(r'^signup/$', base.signup, name="signup"),
    url(r'^signup-pickteam/$', signup_pickteam, name="signup_pickteam"),
    url(r'^home/$', ManageOrderListView.as_view(), name='order_list'),
    url(r'^super_stats/$', SuperStatsView.as_view(), name='super_stats'),
    url(r'^order_list/$', OrderListView.as_view(), name="order_list"),
    url(r'^upload_bulk/$', bulk_orders, name='bulk'),
    url(r'^excel_modal/$', modal_excel_parse_view, name="excel_modal"),
    url(r'^delete_order', base.delete_order, name='delete_order'),
    url(r'^logout/$', base.logout, name='logout'),
    url(r'^temp/$', base.temp, name='temp'),
    url(r'^notify/(?P<notify_id>\w+)', NotifyListView.as_view(), name="notify_list"),
    url(r'^order_confirm/$', base.order_confirm, name='order_confirm'),
    url(r'^manage_orders/$', ManageOrderListView.as_view(), name='manage_orders'),
    url(r'^manage_orders/formats/$', formats_by_retailer, name='manage_orders'),
    url(r'^manage_ws/$', WSFormMixinListView.as_view(), name='manage_ws'),
    url(r'^manage_retailers/$',TCRetailersListView.as_view(), name='manage_retailers'),
    url(r'^delete_wsbyuser/$', delete_wsbygroup, name='delete_wsbyuser'),
    url(r'^edit_wsbyuser/$', edit_wsbyuser, name='edit_wsbyuser'),
    url(r'^add_bulkws/$', bulk_add_ws, name='bulk_add_ws'),
    url(r'^edit_order_format/$', edit_order_format, name='edit_order_format'),
    url(r'^manage_ws/buildings/$', floors_by_building, name='floors_by_buliding'),
    url(r'^check_duplicate_username/$', checks.check_signup, name='check_signup'),
    url(r'^check_business_number/$', checks.check_business_number, name='check_business_number'),
]