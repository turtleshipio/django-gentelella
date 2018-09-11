from app.models import *
from app.views.parsers import *

parser = None


user = TCUser.objects.get(username='kimbs')
parser = FruitsParser(user=user, file=None, local=True)
parser.extract()
