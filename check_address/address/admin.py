from django.contrib import admin
from address.models import *
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(AddressFile)
admin.site.register(AddressText)