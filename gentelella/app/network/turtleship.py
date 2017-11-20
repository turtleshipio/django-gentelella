import requests
import json
from app.models.order import Order

class APIService(object):

    base_url = ""
    dev_domain = "http://dev.turtleship.io/"
    prod_domain = "https://api.turlteship.io/"

    app_default="turtlechain/"

    token = None
    headers = {}

    def __init__(self, token=None, prod=True, version=0):

        if token is not None:
            self.headers = {'Authorization' : '{token}'.format(token=token)}

        if prod:
            self.base_url = "{prod_domain}{app_default}v{version}/"\
                .format(prod_domain=self.prod_domain, app_default=self.app_default, version=str(version))
        else:
            self.base_url = "{dev_domain}{app_default}v{version}/" \
                .format(dev_domain=self.dev_domain, app_default=self.app_default, version=str(version))


    def get_orders_by_retailer_name(self):

        url = "{url}orders/{retailer_idx}".format(url=self.base_url, retailer_idx=str(0))

        params = {'today':'true'}
        r = requests.get(url=url, headers=self.headers, params=params)

        response  = json.loads(r.text)
        li = response['data']['orders']

        orders = [Order(o) for o in li]
        return orders

