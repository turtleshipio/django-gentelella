from django.views.generic import TemplateView
from braces.views import GroupRequiredMixin
from app.custom_db import execute_custom_query
from app.models import *
import time



class SuperStatsView(TemplateView):

    context_object_name = 'data'
    template_name = "app/super_stats.html"
    group_required = [u"staff"]
    login_url = '/'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        ws_count = self.get_ws_count_super()
        retailer_count = TCRetailer.objects.count()
        orders_data = self.get_order_counts_by_date()

        data = {
            'ws_count' : ws_count,
            'retailer_count' : retailer_count,
            'graph_data' : orders_data['graph_data'],
            'acc_orders_value' : orders_data['acc_orders_value'],
            'acc_orders_count' : orders_data['acc_orders_count'],
        }

        context['data'] = data
        return context

    def get_ws_count_super(self):

        query = "SELECT COUNT(DISTINCT(`ws_name`)) FROM `wsbytcgroup`"
        row = execute_custom_query(query)
        return row[0]

    def get_order_counts_by_date(self):
        query = "SELECT DISTINCT(TIMESTAMP(DATE(date_format(created_time,'%Y-%m-%d')))), COUNT(*), SUM(price) FROM orders GROUP BY DATE(date_format(created_time,'%Y-%m-%d'))"
        rs = execute_custom_query(query, fetchone=False)
        li = []
        acc_count = 0
        total_sum = 0

        for dt, count, price_sum in rs:
            acc_count += count
            total_sum += price_sum

            li.append([int(time.mktime(dt.timetuple()))*1000, acc_count])


        result = {
            'graph_data' : li,
            'acc_orders_value': total_sum,
            'acc_orders_count' : acc_count,
        }

        print(result['graph_data'])
        return result

