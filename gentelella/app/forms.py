from django import forms
from django import db
from django.forms import ModelForm
from app import models


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='엑셀파일을 업로드해주세요',
        help_text='max. 42 megabytes'
    )


class OrderListDeleteForm(forms.Form):
    order_id = forms.IntegerField()


class SignUpForm(forms.Form):
    username = forms.CharField()
    name = forms.CharField()
    phone = forms.CharField()
    password = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    acc_type = forms.ChoiceField()
    #acc_type = form.cleaned_data['account-type']
    print(":*******************************")
    print(":*******************************")
    print(":*******************************")
    print(acc_type)


class CreditForm(forms.Form):

    choice = forms.CharField()