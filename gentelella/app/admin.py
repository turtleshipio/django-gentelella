from django.contrib import admin
from app.user_admin import TCUserAdmin
# Register your models here.
from .models import *
from django.contrib.auth.models import Permission

admin.site.register(TCUser, TCUserAdmin)
admin.site.register(TCRetailer)
admin.site.register(TCPickteam)
admin.site.register(Permission)
