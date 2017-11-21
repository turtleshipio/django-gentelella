from django.conf.urls import url
from app.views import base, upload
from app.views.order_list import OrderListView
from app.views.credit_list import CreditListView

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^.*\.html', base.gentella_html, name='gentella'),
    url(r'^$', base.index, name='index'),
    url(r'^order_list', OrderListView.as_view(), name="order_list"),
    url(r'^upload_bulk', upload.bulk_orders, name='bulk'),
    url(r'^credits', CreditListView.as_view(), name='credits'),
    url(r'^delete_order', base.delete, name='delete_order'),
]