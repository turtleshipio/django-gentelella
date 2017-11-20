# -*- coding: utf-8 -*-
class Order(object):

    ws_name = ""
    product_name = ""
    sizeNcolor = ""
    price = ""
    count = -1
    status = ""
    oos = ""
    updated_time = ""
    created_time = ""
    order_id = ""
    retailer_idx = -1


    def __init__(self, data):

        self.set_data(data)


    def set_data(self, data):

        self.ws_name = data['ws_name']
        self.product_name = data['product_name']
        self.sizeNcolor = data['sizeNcolor']
        self.price = "{0}원".format(format(data['price'], ","))
        self.count = data['count']
        self.oos = data['oos']
        self.updated_time = data['updated_time']
        self.created_time = data['created_time']
        self.order_id = data['order_id']
        self.retailer_idx = data['retailer_idx']

        self.status = data['status']


    def __str__(self):
        return self.ws_name