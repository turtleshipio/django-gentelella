from django import forms

class CreateOrderFormatForm(forms.Form):

    retailer = None

    def __init__(self, retailer):
        super().init__(self)
        self.retailer = retailer

    fmt_name        = forms.CharField(max_length=30)
    fmt_ws_name     = forms.CharField(max_length=30)
    fmt_product_name= forms.CharField(max_length=30)
    fmt_sizeNcolor  = forms.CharField(max_length=30)
    fmt_color       = forms.CharField(max_length=30)
    fmt_price       = forms.CharField(max_length=30)
    fmt_count       = forms.CharField(max_length=30)
    fmt_request     = forms.CharField(max_length=30)
