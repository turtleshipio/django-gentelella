import xlrd
from app.models import *


fname ="app/gmv1.csv"

workbook = xlrd.open_workbook(fname)

sheet = workbook.sheet_by_index(0)

print(sheet.nrows)
