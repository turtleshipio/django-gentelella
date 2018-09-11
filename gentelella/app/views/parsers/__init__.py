from app.models import *
from app.utils import check_whitespace

import xlrd


class BaseParser(object):

    user = None
    sheet = None

    sheet_index = 0
    fail_count = 0
    orders = None

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

    head = {}

    def __init__(self, user, file, sheet_index=0, local=False):

        self.user = user
        self.group = TCGroup.objects.filter(main_user=user)[0]
        self.file = file
        self.local = local
        self.sheet_index = sheet_index
        self.sheet = self._get_sheet()

    def _get_sheet(self):

        try:
            if not self.local:
                book = xlrd.open_workbook(file_contents=self.file.read())
                print("???")
            else:
                book = xlrd.open_workbook("test.xlsx", "r")
                print("!!")
                print(book)
            sheet = book.sheet_by_index(self.sheet_index)
            return sheet

        except xlrd.XLRDError:
            raise xlrd.XLRDError

    def inspect_header(self, format):
        self.required = []

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
            required = [r for r in required if bool(r or not r.isspace()) and r != '']

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

        ws_list = WsByTCGroup.objects.exclude(is_deleted=True).filter(group=self.group)

        for nrow in range(1, self.sheet.nrows):
            row = self.sheet.row_values(nrow)

            try:
                datetime = row[self.head[self.optional_fmt['fmt_datetime']]] if 'fmt_datetime' in self.optional_fmt else None

                count = row[self.head[self.required_fmt['fmt_count']]]
                price = row[self.head[self.required_fmt['fmt_price']]]

                count = self._format_numeric(count)
                price = self._format_numeric(price)

                sizencolor = self._format_sizeNcolor(row)

                ws_name = str(row[self.head[self.required_fmt['fmt_ws_name']]]).strip()
                product_name = str(row[self.head[self.required_fmt['fmt_product_name']]])

                ws, ws_phone, building, floor, location = self._get_ws(ws_name, ws_list)

                order = {
                    'sizencolor' : sizencolor,
                    'ws_phone' : ws_phone,
                    'ws_name' : ws_name,
                    'product_name' : product_name,
                    'building' : building,
                    'floor' : floor,
                    'location' : location,
                    'price' : price,
                    'count' : count,
                    'datetime' : datetime,
                }

                orders.append(order)
                msg = ""

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

        self.orders = orders
        return orders, success, msg

    def verbose(self):
        for order in self.orders:
            order = [o if o is not None else '' for o in order.values()]
            print('\t'.join(order))

    def _get_ws(self, ws_name, ws_list):
        ws = None
        for w in ws_list:
            if w.ws_name == ws_name:
                ws = w

        ws_phone = building = floor = location = None

        if ws is not None:
            ws_phone = ws.ws_phone
            building = ws.building
            floor = ws.floor
            location = ws.location

        return ws, ws_phone, building, floor, location

    def _format_numeric(self, data):

        if type(data) == str:
            data = int(data) if data.isdigit() else data
        elif type(data) == float:
            data = int(data)

        data = '%d' % int(data)

        return data

    def _format_sizeNcolor(self, row):

        size = str(row[self.head[self.required_fmt['fmt_sizeNcolor']]])
        if 'fmt_color' in self.required_fmt and self.required_fmt['fmt_color'] is not None and self.required_fmt['fmt_color'] != '':
            color = str(row[self.head[self.required_fmt['fmt_color']]])
        else:
            color = None

        if color is not None:
            sizencolor = ' '.join([size, ' / ', color])
        else:
            sizencolor = size

        return sizencolor


class FruitsParser(BaseParser):

    head = {}

    required = {
        '품명': None,
        '칼라' : None,
        '사이즈' : None,
        '사입가' : None,
        '수량' : None,
    }

    optional = { '날짜': None}

    has_datetime = False
    datetime = None

    def __init__(self, user, file, local):
        super().__init__(user=user, file=None, local=True)
        self.inspect_header()

    def inspect_header(self, format=None):

        # We are not going to inspect. This parser is custom to retailers.

        header = self.sheet.row_values(0)

        for req in self.required:
            for col in header:
                if req == col:
                    self.head[req] = header.index(col)

        for opt in self.optional:
            for col in header:
                print(header)
                if opt == col:
                    self.head[opt] = header.index(col)
                if col == "날짜":
                    self.has_datetime = True

        if self.has_datetime:
            self.datetime = self.sheet.row_values(4)[self.head['날짜']]

        self.has_datetime = False

        return True, "성공"

    def extract(self):

        orders = []

        ws_list = WsByTCGroup.objects.exclude(is_deleted=True).filter(group=self.group)
        ws_name = None
        msg = ""

        for nrow in range(1, self.sheet.nrows):

            order = {}
            row = self.sheet.row_values(nrow)


            if self._is_sub_header(row):
                ws_name = self._get_ws_name(row).strip()
            elif self._is_order_row(row):
                product_name = row[self.head['품명']]
                color = row[self.head['칼라']]
                size = row[self.head['사이즈']]
                price = row[self.head['사입가']]
                count = row[self.head['수량']]


                sizencolor = ' / '.join([size, color])

                price = self._format_numeric(price)
                count = self._format_numeric(count)

                ws, ws_phone, building, floor, location = self._get_ws(ws_name, ws_list)

                order['ws_name'] = ws_name
                order['product_name'] = product_name
                order['sizencolor'] = sizencolor
                order['price'] = price
                order['count']  = count

                order['ws_phone'] = ws_phone if ws_phone is not None else ""
                order['building'] = building if building is not None else ""
                order['floor'] = floor if floor is not None else ""
                order['location'] = location if location is not None else ""

                if self.has_datetime:
                    order['datetime'] = self.datetime

                orders.append(order)
                msg = ""
            else:
                continue

        success = True
        if len(orders) < 1:
            if msg is None:
                msg = "에러가 생겼습니다"
            success = False
        if msg is None:
            msg = ""

        self.orders = orders


        return orders, self.has_datetime, success, msg

    def _get_ws_name(self, row):
        row = row[0].split(' ')

        for col in row:
            if col.startswith("010") or col.startswith("02"):
                return row[row.index(col)-1]

    def _is_sub_header(self, row):

        for i in range(len(row)):

            # first column should not be empty,
            if i == 0 and check_whitespace(row[i]):
                return False

            # this runs from second column, and they should all be empty if sub header
            if i > 0 and not check_whitespace(row[i]):
                return False

        return True

    def _is_order_row(self, row):

        for i in range(len(row)):

            # first column should be empty
            if i == 0 and not check_whitespace(row[i]):
                return False

            # this runs from second column, and they should all be filled if order
            if i > 0 and check_whitespace(row[i]):
                return False

        return True


