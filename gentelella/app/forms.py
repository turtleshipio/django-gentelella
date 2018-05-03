from django import forms
from django import db
from django.forms import ModelForm
from app import models
from app.models import TCUser

class TCUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = TCUser
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


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