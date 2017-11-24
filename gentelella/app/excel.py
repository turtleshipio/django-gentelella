import xlrd
from app.models import Orders
from django.db import transaction

class UploadManager:

    file = None
    book = None
    sheet = None
    retail_user = None
    sheet_name="발주발송관리"
    col_count = 64
    nrows = 0

    fail_count = 0

    required = ['상품주문번호', '주문번호', '배송방법', '택배사', '송장번호', '판매채널',
                '구매자명', '구매자ID', '수취인명', '결제위치', '상품번호', '상품명', '옵션정보',
                '수량', '상품가격', '판매자 상품코드', '구매자연락처',  '우편번호',
                '출고지', '결제수단', '유입경로', '배송지', ]

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
            required = self.required
            diff = set(required) - set(header)

            if diff != set():
                cols = ', '.join([diff])
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

    def insert_db(self):

        orders = []
        msg = ""

        for nrow in range(1, self.sheet.nrows):
            row = self.sheet.row_values(nrow)

            try:
                order = Orders(
                    username=self.retail_user['username'],
                    retailer_id=2,
                    sizencolor= row[self.head['옵션정보']],
                    excel_origin='naver',
                    naver_order_id=row[self.head['주문번호']],
                    naver_order_group_id=row[self.head['상품주문번호']],
                    buyer_name=row[self.head['구매자명']],
                    buyer_id=row[self.head['구매자ID']],
                    receiver_name=row[self.head['수취인명']],
                    pay_origin=row[self.head['결제위치']],
                    product_num=row[self.head['상품번호']],
                    buyer_phone= row[self.head['구매자연락처']],
                    product_name_retailer=row[self.head['상품명']],
                    buyer_pay_method=row[self.head['결제수단']],
                    buyer_address=row[self.head['배송지']],
                    depart_loc=row[self.head['출고지']],
                    postal_code=row[self.head['우편번호']],
                    retailer_price=row[self.head['상품가격']],
                    delivery_method=row[self.head['배송방법']],
                    delivery_id=row[self.head['송장번호']],
                    deliverer=row[self.head['택배사']],
                    sales_channel=row[self.head['판매채널']],
                    marketing_channel=row[self.head['유입경로']],
                    buyer_order_count=row[self.head['수량']],

                       )

                orders.append(order)

            except ValueError:
                self.fail_count += 1
                msg = str(e)

            except Exception as e:
                self.fail_count += 1
                msg = str(e)
                continue

        Orders.objects.bulk_create(orders)

        return self.fail_count, msg




