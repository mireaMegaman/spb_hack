from django.forms import ModelForm
from address.models import *


class AddressTextForm(ModelForm):
    class Meta:
        model = AddressText
        fields = ['text']


class AddressFileForm(ModelForm):
    class Meta:
        model = AddressFile
        fields = ['file']