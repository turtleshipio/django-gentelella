from django import forms

class CreateWsForm(forms.Form):

    retailer = None

    def __init__(self, retailer):
        super().init__(self)
        self.retailer = retailer

        print("heyheeyheyeheyheyehey")

    ws_name = forms.CharField(max_length=30)
    building_name = forms.CharField(max_length=30)
    location = forms.CharField(max_length=30)
    floor = forms.CharField(max_length=30)
    ws_phone = forms.CharField(max_length=30)
