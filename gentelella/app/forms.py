from django import forms


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