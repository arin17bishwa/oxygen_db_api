from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.


class Volunteer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=64, blank=False)
    email=models.EmailField(unique=True,blank=False,null=False)
    contact = PhoneNumberField(blank=False,unique=True)
    alt_contact = PhoneNumberField(blank=True, null=True)
    address = models.TextField(blank=False)
    pin_code = models.IntegerField()
    rating = models.FloatField(default=0)
    is_active = models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return 'Volunteer: {}({}) at {}({})'.format(self.name, self.contact, self.pin_code, self.address)


class Provider(models.Model):
    name = models.CharField(max_length=64, blank=False)
    contact = PhoneNumberField(blank=False,unique=True)
    alt_contact = PhoneNumberField(blank=True, null=True)
    address = models.TextField(blank=False)
    pin_code = models.IntegerField()
    rating = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Provider: {}({}) at {}({})'.format(self.name, self.contact, self.pin_code, self.address)


class DeliveryExecutive(models.Model):
    name = models.CharField(max_length=64, blank=False)
    contact = PhoneNumberField(blank=False, unique=True)
    alt_contact = PhoneNumberField(blank=True, null=True)
    address = models.TextField(blank=False)
    pin_code = models.IntegerField()
    vehicle_type=models.CharField(max_length=64)
    rating = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Delivery: {}({}) at {}'.format(self.name,self.contact,self.pin_code)


@receiver(post_save,sender=User)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        _=Token.objects.create(user=instance)
