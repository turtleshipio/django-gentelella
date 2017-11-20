from django.conf.urls import url
from app.views import base, upload
from app.views.order_list import  order_list

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^.*\.html', base.gentella_html, name='gentella'),
    url(r'^$', base.index, name='index'),
    url(r'^order_list', order_list, name="order_list"),
    url(r'^upload_bulk', upload.bulk_orders, name='bulk'),
]