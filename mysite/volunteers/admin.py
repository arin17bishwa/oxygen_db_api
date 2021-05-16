from django.contrib import admin
from .models import Volunteer, Provider

# Register your models here.
admin.site.register((Volunteer, Provider))
