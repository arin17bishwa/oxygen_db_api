from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
GENDER=[
    ('M','Male'),
    ('F','Female'),
    ('O','Other'),
    ('N','Prefer not to disclose'),
]


class Patient(models.Model):
    name = models.CharField(max_length=64, blank=False)
    gender = models.CharField(max_length=8, choices=GENDER)
    age=models.PositiveSmallIntegerField()
    spo2=models.FloatField()
    status=models.CharField(max_length=64)
    contact = PhoneNumberField(blank=False)
    alt_contact = PhoneNumberField(blank=True, null=True)
    address = models.TextField(blank=False)
    pin_code = models.IntegerField()

    def __str__(self):
        return '{}({},{}) at {}'.format(self.name,self.gender,self.age,self.pin_code)
