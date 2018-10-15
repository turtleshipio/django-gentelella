import requests
import json
from app.models import Order
from app import utils
from datetime import datetime
from app.models import *


class KakaoMessageSender:



    def __init__(self, tmplId="5"):
        self.template = KakaoTemplates.objects.get(tmplId=tmplId)
        self.kakao_msg = self.template.org_msg
        self.notify_url = self.template.cta
        self.smsMsg = ""

    def clear(self):
        self.kakao_msg = ""
        self.notify_url = ""

    def set_msg(self, notify_id, retailer_name, ws_name, phone):
        order_num = notify_id[:7]
        self.kakao_msg = self.kakao_msg.format(order_num=order_num, retailer_name=retailer_name, ws_name=ws_name, phone=phone)
        self.kakao_msg = self.kakao_msg.replace("\\n", "\n")
        self.smsMsg = self.kakao_msg
        self.notify_url = self.notify_url.format(notify_id=notify_id)
        self.template.button1['url_mobile'] = self.notify_url
        self.template.button1['url_pc'] = self.notify_url

        print("!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!")
        print(self.kakao_msg)
        print("!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!")
    def send_kakao_msg(self, phn, prod=True):

        if phn == "010-8895-8454" or phn == "01088958454":
            self.template.button1['url_mobile'] += "&special=true"
            self.template.button1['url_pc'] += "&special=true"

        data = [{
            'userId': self.template.userId,
            'message_type': self.template.message_type,
            'profile': self.template.profile,
            'phn' : self.template.phn,
            'msg': self.kakao_msg,
            'smsKind': self.template.smsKind,
            'tmplId' : self.template.tmplId,
            'msgSms': self.smsMsg,
            'smsSender': self.template.smsSender,
            'reserveDt': self.template.reserveDt,
            'button1': self.template.button1,
        }]



        url = self.template.target_url['prod'] if prod else self.template.target_url['dev']

        try:
            response = requests.post(url=url, headers=self.template.headers, data=json.dumps(data))


        except requests.exceptions.HTTPError as e:
            print(str(e))

class KakaoNotifySender:

    def __init__(self, tmplId=None):
        pass


    target_url = {
        'dev': 'https://dev-alimtalk-api.bizmsg.kr:1443/v1/sender/send',
        'prod': 'https://alimtalk-api.bizmsg.kr/v1/sender/send'
    }

    env = ""
    userId = 'syum'
    message_type = 'at'
    phn = '821088958454'
    profile = '038086c8c247154ec2b8a803ae7322af14cf1d48'
    tmplId = '4'
    #org_msg = '주문번호:{order_id}\n{retailer_name}에서 \
    # {prd1} 외 {prd_count}개의 상품목록에 대해서 주문요청을 했습니다. \
    # 주문을 승인하시면 소매점의 사입삼촌이 해당 매장을 오늘 방문합니다. \
    # 주문요청을 승인하시겠습니까?'

    org_msg = '주문자:{retailer_name}\n도매명:{ws_name}\n\n주문확인 버튼을 클릭후 주문을 확인해 주세요.\n\n주문번호:{order_num}'

    kakao_msg = ""
    smsKind = 'S'
    msgSms = org_msg
    smsSender = '01088958454'
    reserveDt = '00000000000000'
    notify_url = 'http://manage.turtleship.io/notify/{notify_id}'
    button1 = {
        'name': '주문확인',
        'type': 'WL',
        'url_mobile' : ''
    }

    smsMsg = "{otp}"

    sms_msg = ""
    path = "v1/sender/send"
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}


    def clear(self):
        self.kakao_msg = ""
        self.button1['url_mobile'] = ""
        self.phn = ""


    def set_msg(self, retailer_name, ws_name, notify_id, phone=None):

        order_num = notify_id[:7]
        self.kakao_msg = self.org_msg.format(order_num=order_num, retailer_name=retailer_name, ws_name=ws_name)
        notify_url = self.notify_url.format(notify_id=notify_id)
        self.button1['url_mobile'] = notify_url

    def set_sms(self, otp):
        self.smsMsg = self.smsMsg.format(otp=otp)
        return self.smsMsg
    def send_sms(self, sms_msg, phone):
        url = self.target_url['prod'] + self.path
        headers = {'content-type': 'application/json'}

        d = [{
            'userId' : self.userId,
            'message_type' : self.message_type,
            'phn' : phone,
            'profile' : self.profile,
            'tmplId' : self.tmplId,
            'msg' : sms_msg,
            'smsKind' : 'L',
            'msgSms' : sms_msg,
            'smsSender' : '01088958454',
            'smsLmsTit' : '[터틀체인 인증번호]',
            'smsOnly' : 'Y',

        }]


        response = requests.post(url, headers=self.headers, data=json.dumps(d))
        print(response.text)
        return response.text

    def send_kakao_msg(self, phn, prod=True):

        if phn == "010-8895-8454":
            self.button1['url_mobile'] += "&special=true"
        print("????????????")
        print("????????????")
        print("????????????")
        print(self.kakao_msg)
        print("????????????")
        print("????????????")
        print("????????????")
        print("????????????")
        print("????????????")
        data = [{
            'userId': self.userId,
            'message_type': self.message_type,
            'profile': self.profile,
            'phn' : phn,
            'msg': self.kakao_msg,
            'smsKind': self.smsKind,
            'tmplId' : self.tmplId,
            'msgSms': self.smsMsg,
            'smsSender': self.smsSender,
            'reserveDt': self.reserveDt,
            'button1': self.button1,
        }]



        url = self.target_url['prod'] if prod else self.target_url['dev']

        try:
            response = requests.post(url=url, headers=self.headers, data=json.dumps(data))


        except requests.exceptions.HTTPError as e:
            print(str(e))



class OrderCreator:

    notifies = {}
    orders = []
    phones = []
    phone_dict = {}
    ws_dict = {}
    ws_list = []


    def create_orders_from_js(self, user, orders_js, username, retailer_name, pickteam_id, org):

        self.notifies = {}
        self.orders = []
        self.ws_list = []
        ws = None

        for index, order_js in enumerate(orders_js):

            ws_name = order_js['ws_name']
            if ws_name not in self.ws_list:
                try:
                    ws = WsByTCGroup.objects.exclude(is_deleted=True).get(org=org, ws_name=ws_name)
                    self.ws_list.append(ws_name)
                except Exception as e:
                    print(str(e))
                    print("!!!!!!!!")
                    print("!!!!!!!!")
                    print("!!!!!!!!")
                    print("!!!!!!!!")
                    print("!!!!!!!!")
                    print("!!!!!!!!")
                    print("!!!!!!!!")
                    print("!!!!!!!!")
                    print("!!!!!!!!")
            timestamp = datetime.now().timestamp()
            timestamp *= 1000000
            timestamp = str(int(timestamp))
            index = str(index)
            product_name = order_js['product_name']


            if ws_name not in self.notifies:
                notify_id = utils.create_notify_id(timestamp, index, ws_name, retailer_name, product_name)
                self.notifies[ws_name] = {
                    'phone': order_js['ws_phone'],
                    'notify_id': notify_id}
            else:
                notify_id = self.notifies[ws_name]['notify_id']

            if ws is None:
                print("#####")
                print("#####")
                print("#####")
                print(ws_name)
                print("#####")
                print("#####")
                print("#####")
                print("#####")
                print("#####")
            order = Order(
                username=username,
                sizencolor=order_js['sizencolor'],
                ws_phone=ws.ws_phone if ws is not None else None,
                ws_name=ws_name,
                product_name=order_js['product_name'],
                building=ws.building if ws is not None else None,
                floor= ws.floor if ws is not None else None,
                location= ws.location if ws is not None else None,
                count=order_js['count'],
                price=order_js['price'],
                is_deleted=False,
                status="onwait",
                notify_id=notify_id,
                pickteam_id=pickteam_id,
                retailer_name=retailer_name,
                created_time = datetime.strptime('2018-10-11', '%Y-%m-%d'),
                created_date = datetime.strptime('2018-10-11', '%Y-%m-%d').date(),
                #created_time = datetime.now(),
                #created_date = datetime.now().date(),
                #created_time = order_js['datetime'],
            )
            self.orders.append(order)

        try:
            Order.objects.bulk_create(self.orders)
            return True
        except Exception as e:
            print("!!!!")
            print("!!!!")
            print("!!!!")
            print(str(e))
            print("!!!!")
            print("!!!!")
            print("!!!!")
            return False

