from app.models.orders import Order, OrderGroup

class OrderSerializer(object):

    order = None

    def __init__(self, data):
        self.order = Order()

        self.order.ws_name = data['ws_name']
        self.order.product_name = data['product_name']
        self.order.sizeNcolor = data['sizeNcolor']
        self.order.updated_time = data['updated_time']
        self.order.created_time = data['created_time']
        self.order.status = data['status']
        self.order.price = data['price']
        self.order.count = data['count']
        self.order.phone = data['phone']
        self.order.oos = data['oos']
        self.order.order_id = data['order_id']


class OrderGroupSerializer(object):

    ordergroup_id = -1
    retailer_idx = -1
    user_idx = -1
    updated_time = ""
    created_time = ""