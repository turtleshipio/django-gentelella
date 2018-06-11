import xlrd
from app.models import Order, Notify
from django.db import transaction
import random
import string
from random import randint
import requests

class UploadManager:

    file = None
    book = None
    sheet = None
    retail_user = None
    sheet_name="발주발송관리"
    col_count = 64
    nrows = 0


    notify = {}
    fail_count = 0
    '''
    #required = ['상품주문번호', '주문번호', '배송방법', '택배사', '송장번호', '판매채널',
                '구매자명', '구매자ID', '수취인명', '결제위치', '상품번호', '상품명', '옵션정보',
                '수량', '상품가격', '판매자 상품코드', '구매자연락처',  '우편번호',
                '출고지', '결제수단', '유입경로', '배송지', ]'''
    required = ['도매명','층', '전화번호', '상가',  '호수', '수량', '사이즈', '컬러', '도매가', '장끼명']

    head = {}

    def set_file(self, file):

        try:
            self.book = xlrd.open_workbook(file_contents=file.read())
            self.sheet = self.book.sheet_by_index(0)
            self.nrows = self.sheet.nrows

        except xlrd.XLRDError:
            raise xlrd.XLRDError

    def set_retail_user(self, retail_user):
        self.retail_user = retail_user

    def validate(self):

        try:
            if self.sheet is None:
                return False, "엑셀시트가 올바르지 않습니다."
            if self.sheet_name != self.book.sheet_names()[0]:
                return False, "엑셀시트의 이름은 \"발주발송관리\"여야만 합니다."



            header = self.sheet.row_values(0)

            for h in header:
                h = h.strip()



            required = self.required

            print("**************************")
            print(header)

            diff = set(required) - set(header)
            print("**************************")
            print("diff should be an empty set()")
            print(diff)

            if diff != set():
                diff = list(diff)
                cols = ', '.join(diff)

                return False, "아래의 열 이름들을 확인해주세요\n{cols}".format(cols=cols)
            else:
                for req in required:
                    for col in header:
                        if req == col:
                            self.head[req] = header.index(col)

        except Exception as e:
            return False, str(e)
            #return False, "알 수 없는 이유로 실패했습니다. 엑셀 양식을 다시 한번 확인해주세요"

        return True, "성공"

    def extract(self):

        orders = []
        msg = ""

        nrow = self.sheet.nrows

        for nrow in range(1, self.sheet.nrows):
            row = self.sheet.row_values(nrow)

            try:

                count = row[self.head['수량']]
                price = row[self.head['도매가']]
                print("1111111111111111111")
                print(type(count))
                print(type(price))
                if type(count) == str:
                    count = int(count) if count.isdigit() else count
                elif type(count) == int:
                    continue
                elif type(count) == float:
                    count = int(count)


                if type(price) == str:
                    price = int(price) if price.isdigit() else price
                elif type(price) == int:
                    continue
                elif type(price) == float:
                    price = int(price)

                print("222222222")
                print(type(count))
                print(type(price))


                count = '%d' % int(count)
                price = '%d' % int(price)





                size = str(row[self.head['사이즈']])
                color = str(row[self.head['컬러']])
                ws_phone = str(row[self.head['전화번호']])
                ws_name = str(row[self.head['도매명']])
                product_name = str(row[self.head['장끼명']])
                building = str(row[self.head['상가']])
                floor = str(row[self.head['층']])
                location = str(row[self.head['호수']])

                sizencolor = ' '.join([size, ' / ', color])

                order = {
                    'sizencolor' : sizencolor,
                    'ws_phone': ws_phone,
                    'ws_name': ws_name,
                    'product_name': product_name,
                    'building': building,
                    'floor': floor,
                    'location': location,
                    'price': price,
                    'count' : count
                }

                orders.append(order)
                msg = "success!"


            except ValueError as e:
                msg = str(e)
                continue

            except Exception as e:
                print("exception while excel extracting")
                print(row)
                msg = str(e)
                continue

        success = True
        if len(orders) < 1:
            success = False


        return orders, success, msg



    def insert_db(self):

        orders = []
        msg = ""
        notifies = {}

        for nrow in range(1, self.sheet.nrows):
            row = self.sheet.row_values(nrow)

            try:

                ws_name = row[self.head['도매명']]
                count = row[self.head['수량']]
                if type(count)  == str:
                    count = int(count) if count.isdigit() else count
                elif type(count) == int:
                    continue
                elif type(count) == float:
                    count = int(count)

                count = '%d' % (count)


                if ws_name in notifies:
                    notify_id = notifies[ws_name]
                else:
                    notifies[ws_name] = self.get_uuid(20)
                    #notifies[ws_name] = randint(0,9999)
                    notify_id = notifies[ws_name]

                order = Order(
                    username=self.retail_user['username'],
                    retailer_name = self.retail_user['retailer_name'],
                    retailer_id=self.retail_user['retailer_id'],
                    sizencolor= row[self.head['사이즈 및 컬러']],
                    ws_phone = row[self.head['전화번호']],
                    ws_name = ws_name,
                    product_name = row[self.head['장끼명']],
                    building =row[self.head['상가']],
                    floor=row[self.head['층']],
                    location=row[self.head['호수']],
                    count = count,
                    price = row[self.head['도매가']],
                    is_deleted="false",
                    status="onwait",
                    notify_id=notify_id
                )

                if ws_name not in self.notify:
                    self.notify[ws_name] = {}
                    self.notify[ws_name]['notify_id'] = notify_id
                    self.notify[ws_name]['retailer_id'] = self.retail_user['retailer_id']
                    self.notify[ws_name]['prd_count'] = count
                    self.notify[ws_name]['prd1'] = row[self.head['장끼명']]
                else:
                    if type(count) == int:
                        self.notify[ws_name]['prd_count'] += count

                    #excel_origin='naver',
                    #naver_order_id=row[self.head['주문번호']],
                    #naver_order_group_id=row[self.head['상품주문번호']],
                    #buyer_name=row[self.head['구매자명']],
                    #buyer_id=row[self.head['구매자ID']],
                    #receiver_name=row[self.head['수취인명']],
                    #pay_origin=row[self.head['결제위치']],
                    #product_num=row[self.head['상품번호']],
                    #buyer_phone= row[self.head['구매자연락처']],
                    #product_name_retailer=row[self.head['상품명']],
                    #buyer_pay_method=row[self.head['결제수단']],
                    #buyer_address=row[self.head['배송지']],
                    #depart_loc=row[self.head['출고지']],
                    #postal_code=row[self.head['우편번호']],
                    #retailer_price=row[self.head['상품가격']],
                    #delivery_method=row[self.head['배송방법']],
                    #delivery_id=row[self.head['송장번호']],
                    #deliverer=row[self.head['택배사']],
                    #sales_channel=row[self.head['판매채널']],
                    #marketing_channel=row[self.head['유입경로']],
                    #buyer_order_count=row[self.head['수량']],

                    #   )

                orders.append(order)


            except ValueError as e:
                self.fail_count += 1
                msg = str(e)
                continue

            except Exception as e:
                self.fail_count += 1
                msg = str(e)
                continue

        Order.objects.bulk_create(orders)

        return self.fail_count, msg

    def get_uuid(self, n):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(n))

    def notify_orders(self):

        notifies = []

        msg = ""

        for ws in self.notify:

            try:
                n = Notify(
                    ws_name=ws,
                    notify_id=self.notify[ws]['notify_id'],
                    retailer_id=self.notify[ws]['retailer_id'],
                    prd1=self.notify[ws]['prd1'],
                    prd_count=self.notify[ws]['prd_count']
                )

                notifies.append(n)

            except ValueError:
                msg = str(e)

            except Exception as e:
                msg = str(e)
                continue

        Notify.objects.bulk_create(notifies)







