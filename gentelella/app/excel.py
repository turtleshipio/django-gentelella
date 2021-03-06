import xlrd
from django.utils.dateparse import parse_date
from app.models import *

import hgtk


class BulkAddWsManager:



    required_fmt = {
        'fmt_ws_name': None,
        'fmt_building': None,
        'fmt_floor' : None,
        'fmt_location' : None,
        'fmt_col' : None,
        'fmt_mobile_phone' : None,
        'fmt_ws_phone' : None,
    }

    optional_fmt = {
        'fmt_ws_phone' : None,
        'fmt_ws_phone_second' : None,
    }

    ws_list = None
    group = None

    def __init__(self, user):
        self.user = user
        self.group = TCGroup.objects.get(group_id=3, main_user=user)


    def set_file(self, file):

        try:
            self.book = xlrd.open_workbook(file_contents=file.read())
            self.sheet = self.book.sheet_by_index(0)
            self.nrows = self.sheet.nrows

        except xlrd.XLRDError:
            raise xlrd.XLRDError

    def test(self):
        self.ws_list = []

        for nrow in range(1, self.sheet.nrows):
            row = self.sheet.row_values(nrow)

            ws_name = row[self.head_ws_name]
            building = row[self.head_building]
            location = row[self.head_location]
            location = str(location).split('.')[0]
            floor = row[self.head_floor]
            floor = str(floor).split('.')[0]
            col  = row[self.head_col]
            col = str(col).split('.')[0]
            ws_phone = row[self.head_phone]
            ws_phone_second = row[self.head_second_phone]

            s = ', '.join([ws_name, building, location, floor, col, ws_phone, ws_phone_second])
            print(s)


    def validate(self):

        try:
            if self.sheet is None:
                return False, "엑셀시트가 올바르지 않습니다."
            header = self.sheet.row_values(0)

            print("!!!!")
            print("!!!!")
            print("!!!!")
            print("!!!!")
            print(header)
            print("!!!!")
            print("!!!!")
            print("!!!!")
            required_format = BulkAddWsFormat.objects.filter(required=True).values_list("format", flat=True)
            optional_format = BulkAddWsFormat.objects.filter(required=False).values_list("format", flat=True)

            diff = set(required_format) - set(header)

            if diff != set():
                cols = ', '.join(diff)
                return False, "아래의 열 이름들을 확인해주세요\n{cols}".format(cols=cols)
            else:
                for fmt in required_format:
                    for col in header:
                        if fmt == col:
                            self.head[fmt] = header.index(col)
                for fmt in optional_format:
                    for col in header:
                        if  fmt == col:
                            self.head[fmt] = header.index(col)


        except Exception as e:
            return False, str(e)

        return True, "success"



    def extract(self):
        self.ws_list = []

        for nrow in range(1, self.sheet.nrows):

            row = self.sheet.row_values(nrow)
            try:
                ws_name = row[self.head_ws_name]
                building = row[self.head_building]
                location = row[self.head_location]
                location = str(location).split('.')[0]
                floor = row[self.head_floor]
                floor = str(floor).split('.')[0]
                col  = row[self.head_col]
                col = str(col).split('.')[0]
                ws_phone = row[self.head_phone]
                ws_phone_second = row[self.head_second_phone]


                ws = WsByTCGroup(
                    ws_name=ws_name,
                    building=building,
                    location = location,
                    floor = floor,
                    col = col,
                    ws_phone = ws_phone,
                    ws_phone_second = ws_phone_second,
                    group = self.group
                )

                self.ws_list.append(ws)
            except Exception as e:
                print(', '.join(row))

        WsByTCGroup.objects.bulk_create(self.ws_list)






class FastValidator:

    user = None
    file = None
    sheet = None

    required_fmt = ["도매명", "상품명", "사이즈", "컬러", "도매가", "수량"]


    required_fmt = {
        'fmt_ws_name' : "매장명",
        'fmt_product_name' : "품명",
        'fmt_sizeNcolor' : "사이즈",
        'fmt_price' : "가격",
        'fmt_count' : "수량",
        'fmt_color' : "칼라",
    }
    head = {}

    def __init__(self, user):
        self.user = user

    def set_file(self, file):

        try:
            self.book = xlrd.open_workbook(file_contents=file.read())
            self.sheet = self.book.sheet_by_index(0)
            self.nrows = self.sheet.nrows

        except xlrd.XLRDError:
            raise xlrd.XLRDError


    def validate(self):

        self.required = []
        self.head = {}

        try:
            if self.sheet is None:
                return False, "엑셀시트가 올바르지 않습니다."
            header = self.sheet.row_values(0)
            required = list(self.required_fmt.values())
            required = [r for r in required if bool(r or not r.isspace()) and r !='']

            diff = set(required) - set(header)
            if diff != set():
                cols = ', '.join(diff)
                return False, "아래의 열 이름들을 확인해주세요\n{cols}".format(cols=cols)
            else:
                for req in required:
                    for col in header:
                        if req == col:
                            self.head[req] = header.index(col)
        except Exception as e:
            return False, str(e)

        return True, "성공"

    def extract(self):

        orders = []
        msg = ""
        nrow = self.sheet.nrows
        self.ws_dict = {}
        self.ws_list = []
        group = TCGroup.objects.filter(main_user=self.user)[0]

        for nrow in range(1, self.sheet.nrows):
            row = self.sheet.row_values(nrow)

            try:

                count = row[self.head[self.required_fmt['fmt_count']]]
                price = row[self.head[self.required_fmt['fmt_price']]]

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

                count = '%d' % int(count)
                price = '%d' % int(price)

                size = str(row[self.head[self.required_fmt['fmt_sizeNcolor']]])
                if 'fmt_color' in self.required_fmt and self.required_fmt['fmt_color'] is not None and self.required_fmt['fmt_color'] != '':
                    color = str(row[self.head[self.required_fmt['fmt_color']]])
                else:
                    color = None

                ws_name = str(row[self.head[self.required_fmt['fmt_ws_name']]])
                product_name = str(row[self.head[self.required_fmt['fmt_product_name']]])

                if color is not None:
                    sizencolor = ' '.join([size, ' / ', color])
                else:
                    sizencolor = size

                try:
                    if ws_name not in self.ws_list:
                        ws = WsByTCGroup.objects.exclude(is_deleted=True).get(group=group, ws_name=ws_name)
                        self.ws_list.append(ws_name)

                except Exception as e:
                    return None, None, "Does Not Exist"

                order = Order(
                    sizencolor = sizencolor,
                    ws_phone = ws.ws_phone,
                    ws_name = ws_name,
                    product_name = product_name,
                    building = ws.building,
                    floor = ws.floor,
                    location = ws.location,
                    price = price,
                    count = count
                )

                orders.append(order)

            except ValueError as e:
                continue

            except Exception as e:
                continue
            finally:
                Order.objects.bulk_create(orders)



class OrderExcelValidator:

    user = None

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
    required = None

    required_fmt = {
        'fmt_ws_name' : None,
        'fmt_product_name' : None,
        'fmt_sizeNcolor' : None,
        'fmt_price' : None,
        'fmt_count' : None,
        'fmt_color' : None,
    }

    optional_fmt = {
        'fmt_color' : None,
        'fmt_request' : None,
        'fmt_datetime' : None,
    }

    ws_dict = {}
    ws_list = []
    head = {}

    def __init__(self, user):
        self.user = user

    def set_file(self, file):

        #is_index = True
        is_index = False
        try:
            self.book = xlrd.open_workbook(file_contents=file.read())
            index = 0
            fname = "0702"
            print(self.book.sheet_names())
            if fname in self.book.sheet_names():
                print("hey!")
                index = self.book.sheet_names().index(fname)
            if is_index:
                self.sheet = self.book.sheet_by_index(index)
            else:
                self.sheet = self.book.sheet_by_index(0)
            self.nrows = self.sheet.nrows

        except xlrd.XLRDError:
            raise xlrd.XLRDError

    def set_retail_user(self, retail_user):
        self.retail_user = retail_user

    def validate(self, format):

        self.required = []
        self.head=  {}

        for fmt in self.required_fmt:
            if hasattr(format, fmt):
                self.required_fmt[fmt] = getattr(format, fmt)
            else:
                return False, "다음 항목이 업로드해주신 엑셀파일에 존재하지 않습니다:%s" % fmt

        for fmt in self.optional_fmt:
            if hasattr(format, fmt):
                self.optional_fmt[fmt] = getattr(format, fmt)

        try:
            if self.sheet is None:
                return False, "엑셀시트가 올바르지 않습니다."
            header = self.sheet.row_values(0)

            required = list(self.required_fmt.values())
            required = [r for r in required if bool(r or not r.isspace()) and r !='']

            optional = list(self.optional_fmt.values())
            optional = [o for o in optional if bool(o or not o.isspace()) and o != '']

            diff = set(required) - set(header)
            if diff != set():
                cols = ', '.join(diff)
                return False, "아래의 열 이름들을 확인해주세요\n{cols}".format(cols=cols)
            else:
                for req in required:
                    for col in header:
                        if req == col:
                            self.head[req] = header.index(col)

                for opt in optional:
                    for col in header:
                        if opt == col:
                            self.head[opt] = header.index(col)

        except Exception as e:
            return False, str(e)

        return True, "성공"

    def extract(self):

        orders = []
        msg = None
        nrow = self.sheet.nrows
        self.ws_dict = {}
        self.ws_list = []
        group = TCGroup.objects.filter(main_user=self.user)[0]
        has_datetime = False
        ws_list = WsByTCGroup.objects.exclude(is_deleted=True).filter(group=group).values()
        ws_list = [dict(ws) for ws in ws_list]
        ws_name_list = WsByTCGroup.objects.exclude(is_deleted=True).filter(group=group).values_list("ws_name", flat=True)

        for nrow in range(1, self.sheet.nrows):
            row = self.sheet.row_values(nrow)

            try:

                count = row[self.head[self.required_fmt['fmt_count']]]
                price = row[self.head[self.required_fmt['fmt_price']]]

                datetime = row[self.head[self.optional_fmt['fmt_datetime']]] if 'fmt_datetime' in self.optional_fmt else None

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

                count = '%d' % int(count)
                price = '%d' % int(price)

                size = str(row[self.head[self.required_fmt['fmt_sizeNcolor']]])
                if 'fmt_color' in self.required_fmt and self.required_fmt['fmt_color'] is not None and self.required_fmt['fmt_color'] != '':
                    color = str(row[self.head[self.required_fmt['fmt_color']]])
                else:
                    color = None

                ws_name = str(row[self.head[self.required_fmt['fmt_ws_name']]])
                ws_name = ws_name.strip()
                product_name = str(row[self.head[self.required_fmt['fmt_product_name']]])

                if color is not None:
                    sizencolor = ' '.join([size, ' / ', color])
                else:
                    sizencolor = size


                if ws_name in ws_name_list:
                    for w in ws_list:
                        if ws_name == w['ws_name']:
                            ws = w

                    ws = {
                        'ws_phone' : '',
                        'building' : 'APM',
                        'floor' : '3',
                        'location' : '311',
                        'col' : 'C',
                    }

                has_datetime = (datetime is not None)
                order = {
                    'sizencolor' : sizencolor,
                    'ws_phone': ws['ws_phone'],
                    'ws_name': ws_name,
                    'product_name': product_name,
                    'building': ws['building'],
                    'floor': ws['floor'],
                    'location': ws['location'],
                    'price': price,
                    'count' : count,
                    'datetime' :datetime,

                }

                orders.append(order)
                msg = "success!"

            except ValueError as e:
                msg = str(e)
                continue

            except Exception as e:
                msg = str(e)
                continue

        success = True
        if len(orders) < 1:
            if msg is None:
                msg = "에러가 생겼습니다"
            success = False

        if msg is None:
            msg = ""
        return orders, has_datetime, success, msg
