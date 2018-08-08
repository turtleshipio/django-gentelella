from app.models import *
from xlrd import open_workbook

from app.excel import FastValidator, BulkAddWsManager

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




