import requests
import json


class KakaoSender:

    target_url = {
        'dev': 'https://dev-alimtalk-api.bizmsg.kr:1443/v1/sender/send',
        'prod': 'https://alimtalk-api.bizmsg.kr/v1/sender/send'
    }

    env = ""
    userId = 'syum'
    message_type = 'at'
    phn = '821088958454'
    profile = '038086c8c247154ec2b8a803ae7322af14cf1d48'
    tmplId = '2'
    org_msg = '주문번호:{order_id}\n{retailer_name}에서 \
     {prd1} 외 {prd_count}개의 상품목록에 대해서 주문요청을 했습니다. \
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

    smsMsg = "{retailer_name}에서 주문요청이 들어왔습니다. 링크를 눌러 확인하세요 {link}"

    sms_msg = ""
    path = "v1/sender/send"
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def clear(self):
        self.kakao_msg = ""
        self.button1['url_mobile'] = ""
        self.phn = ""


    def set_msg(self, order_id, retailer_name, prd1, prd_count, notify_id):

        self.kakao_msg = self.org_msg.format(order_id=order_id, retailer_name=retailer_name, prd1=prd1, prd_count=prd_count)
        notify_url = self.notify_url.format(notify_id=notify_id)
        self.button1['url_mobile'] = notify_url

    def set_sms(self, retailer_name, notify_id):
        self.smsMsg = self.smsMsg.format(retailer_name=retailer_name, link=self.notify_url.format(notify_id=notify_id))

    def send_sms(self, sms_msg, phone):
        url = self.target_url['prod'] + self.path

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


        response = requests.post(url, headers=self.headers, data=json.dumps(d))

        return response.text

    def send_kakao_msg(self, phn, prod=True):

        headers = {'content-type': 'application/json'}
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
        print(url)
        print(self.button1)
        print(data)

        try:
            response = requests.post(url=url, headers=self.headers, data=json.dumps(data))
            print("***************************************")
            print("***************************************")
            print("***************************************")
            print("***************************************")
            print("***************************************")
            print("***************************************")
            print("***************************************")
            print("***************************************")
            print("***************************************")
            print("***************************************")
            print("***************************************")
            print(response.text)

        except requests.exceptions.HTTPError as e:
            print(str(e))




