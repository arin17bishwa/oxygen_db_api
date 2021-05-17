from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User

from ..models import (Provider,Volunteer,DeliveryExecutive,Product,ProviderProductDetail)


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


class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model=Volunteer
        fields=['pin_code','alt_contact','address']


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model=Provider
        exclude=['rating',]


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model=Product
        fields=['product_type','product_details','uom',]


class ProviderProductSerializer(serializers.ModelSerializer):
    provider_name=serializers.SerializerMethodField('get_provider_name')
    product_name=serializers.SerializerMethodField('get_product_name')

    class Meta:
        model=ProviderProductDetail
        fields=['pin_code','total','product','provider','provider_name','product_name']

    def get_provider_name(self,obj):
        _=self
        try:
            return obj.provider.name
        except Provider.DoesNotExist:
            data={'success':False,'msg':'Provider does not exist'}
            return Response(data=data,status=status.HTTP_404_NOT_FOUND)

    def get_product_name(self,obj):
        _ = self
        try:
            prod = obj.product
            temp=prod.product_details
            if temp!='cylinder':
                return temp
            return '{} | UOM={}'.format(temp,prod.uom)

        except Product.DoesNotExist:
            data = {'success': False, 'msg': 'Product does not exist'}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)


class ProviderProductUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProviderProductDetail
        fields = ['pin_code', 'total']
