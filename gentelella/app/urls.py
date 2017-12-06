from django.conf.urls import url


from app.views import base, upload
from app.views.order_list import OrderListView
from app.views.credit_list import CreditListView
from app.views.notify_list import NotifyListView

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^.*\.html', base.gentella_html, name='gentella'),
    url(r'^$', base.login, name='login'),
    url(r'^login', base.login, name='login'),
    url(r'^signup', base.signup, name='signup'),
    url(r'^home', base.home, name='home'),
    url(r'^order_list', OrderListView.as_view(), name="order_list"),
    url(r'^upload_bulk', upload.bulk_orders, name='bulk'),
    url(r'^credits', CreditListView.as_view(), name='credits'),
    url(r'^delete_order', base.delete_order, name='delete_order'),
    url(r'^logout', base.logout, name='logout'),
    url(r'^notify', base.notify, name="notify"),
    url(r'^list', NotifyListView.as_view(), name="notify_list"),

]