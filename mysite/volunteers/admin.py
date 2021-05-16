from django.contrib import admin
from .models import Volunteer, Provider, DeliveryExecutive,Product,ProviderProductDetail

# Register your models here.
admin.site.register((Volunteer, Provider,DeliveryExecutive,Product,ProviderProductDetail))
