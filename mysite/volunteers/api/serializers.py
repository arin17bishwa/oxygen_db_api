from rest_framework import serializers

from django.contrib.auth.models import User

from ..models import (Provider,Volunteer)


class RegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model=User
        fields=['username','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def save(self):
        account=User(
            username=self.validated_data['username'],
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password!=password2:
            raise serializers.ValidationError({'confirm_password':'Passwords must match'})
        account.set_password(password)
        account.save()
        return account


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=Volunteer
        fields=['name','email','contact','alt_contact','address','pin_code']


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model=Provider
        exclude=['rating',]