from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
VEHICLE_TYPES=[
    (2,'2 WHEELER'),
    (3,'3 WHEELER'),
    (4,'4 WHEELER'),
]

PRODUCT_TYPES=[
    ('oxygen','Oxygen'),
]

PRODUCTS=[
    ('cylinder','Oxygen Cylinder'),
    ('oximeter','Oximeter'),
    ('concentrator', 'Concentrator'),
]


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
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return 'Provider: {}({})'.format(self.name, self.contact)


class DeliveryExecutive(models.Model):
    name = models.CharField(max_length=64, blank=False)
    contact = PhoneNumberField(blank=False, unique=True)
    alt_contact = PhoneNumberField(blank=True, null=True)
    address = models.TextField(blank=False)
    pin_code = models.IntegerField()
    vehicle_type=models.IntegerField(choices=VEHICLE_TYPES,default=2)
    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    def __str__(self):
        return 'Delivery: {}({}) at {}'.format(self.name,self.contact,self.pin_code)


class Product(models.Model):
    product_type=models.CharField(max_length=16,choices=PRODUCT_TYPES)
    product_details=models.CharField(max_length=16,choices=PRODUCTS)
    uom=models.FloatField(default=0.5)  # IN LITRES
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    def __str__(self):
        temp= '{}'.format(self.product_details)
        if temp!='cylinder':
            return temp
        return temp+' | UOM={} L'.format(self.uom)


class ProviderProductDetail(models.Model):
    provider = models.ForeignKey(Provider,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    pin_code=models.IntegerField()
    total=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    def __str__(self):
        return '{} provides {} at {}'. format(self.provider,self.product, self.pin_code)

    class Meta:
        unique_together=('provider','product')


@receiver(post_save,sender=User)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        _=Token.objects.create(user=instance)
