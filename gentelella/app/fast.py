from app.models import *
import xlrd
from app.excel import FastValidator, BulkAddWsManager
from app.utils import check_whitespace

def test_ws_bulk(ws_fname):
    manager = BulkAddWsManager()
    manager.set_file(ws_fname)
    manager.test()


def add_ws_bulk(ws_fname):
    manager = BulkAddWsManager()
    manager.set_file(ws_fname)
    manager.extract()


def upload_orders_fast(fname):

    validator = FastValidator()
    validator.set_file(fname)
    validator.validate()
    validator.extract()

def update_ws_phone():

    user = TCUser.objects.get(username='kimbs')
    group = TCGroup.objects.filter(main_user=user)[0]

    book = xlrd.open_workbook("./app/ws_list.xlsx")
    sheet = book.sheet_by_index(0)

    header = sheet.row_values(0)
    head = {}
    count = 0
    fail = 0
    for col in header:
        if col == "도매명":
            head["ws_name"] = header.index(col)
        if col == "핸드폰 번호":
            head['ws_phone'] = header.index(col)

    for nrow in range(1, sheet.nrows):

        row = sheet.row_values(nrow)
        ws_name = row[head['ws_name']]
        ws_phone = row[head['ws_phone']]

        if not check_whitespace(ws_phone) and ws_phone.startswith("010"):
            ws = WsByTCGroup.objects.filter(ws_name=ws_name, group=group)[0]
            ws.ws_phone = ws_phone
            ws.save()
            count += 1
        else:
            fail += 1

    return count, fail