import requests
import json


class KakaoSender:

    target_url = {
        'dev': 'https://dev-alimtalk-api.bizmsg.kr:1443',
        'prod': 'https://alimtalk-api.bizmsg.kr/'
    }

    userId = 'syum'
    message_type = 'at'
    phn = '821088958454'
    profile = '49299f2c8dad2ad3143ba864754f46666199cf61'
    tmplId = '2'
    org_msg = '주문번호:{order_id}\n{retailer}에서 \
     {prd1} 외 {prd_count}개의 상품수에 대해서 주문요청을 했습니다. \
     주문을 승인하시면 소매점의 사입삼촌이 해당 매장을 오늘 방문합니다. \
     주문요청을 승인하시겠습니까?'
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

    sms_msg = ""
    path = "v1/sender/send"
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def clear(self):
        self.kakao_msg = ""
        self.button1 = ""

    def set_msg(self, order_id, retailer, prd1, prd_count, notify_id):

        self.kakao_msg = self.msg.format(order_id=order_id, retailer=retailer, prd1=prd1, prd_count=prd_count)
        self.button1['url_mobile'] = self.notify_url.format(notify_id=notify_id)

    def set_sms(self, sms_msg):
        self.sms_msg = sms_msg

    def send_sms(self, sms_msg, phone):
        url = self.target_url['prod'] + self.path
        print("?????????????????????????")
        print(url)
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
            'smsLmsTit' : '[터틀체인 주문관리]',
            'smsOnly' : 'Y',

        }]

        print(d)

        response = requests.post(url, headers=self.headers, data=json.dumps(d))

        return response.text

    def send_msg(self, prod=True):

        headers = {'content-type': 'application/json'}
        data = {
            'userId': self.userId,
            'message_type': self.message_type,
            'phn': self.phn,
            'profile': self.profile,
            'msg': self.msg,
            'smsKind': self.smsKind,
            'msgSms': self.msg,
            'smsSender': self.smsSender,
            'reserveDt': self.reserveDt,
            'button1': self.button1,
        }

        url = self.target_url['prod'] if prod else self.target_url['dev']



        try:
            response = requests.post(urlheaders=headers, data=data, url=url)

        except requests.exceptions.HTTPError as e:
            print(str(e))




