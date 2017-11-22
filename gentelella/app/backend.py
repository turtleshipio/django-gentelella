from django.contrib.auth.hashers import check_password
from app.models import RetailUser
from passlib.hash import sha256_crypt
import logging

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import connection

class RetailUserBackend(object):

    _querylogger = logging.getLogger('sql.compiler')

    def authenticated_user(self, request, username=None, password=None):

        if username is None or password is None:
            return None
        try:
            retail_user = RetailUser.objects.get(username=username)
        except RetailUser.DoesNotExist:
            return None

        pwd_valid = sha256_crypt.verify(password, retail_user.password)

        if pwd_valid:
            return retail_user

    def create_user(self, request, username=None, name=None, password=None, phone=None):

        if username is None or password is None or phone is None:
            return False

        try:
            enc_password = sha256_crypt.encrypt(password)
            print(RetailUser.objects.create(username=username,name=name,password=password,phone=phone).query)
            RetailUser.objects.create(username=username, name=name, password=enc_password, phone=phone)
            print(connection.queries)
        except:
            return False

        return True
