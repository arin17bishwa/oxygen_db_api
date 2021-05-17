from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,AllowAny, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter,OrderingFilter
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from ..utils import send_conf_mail,account_activation_token
from ..decorators import vol_active
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from ..models import (
    Provider,
    Volunteer,
    Product,
    ProviderProductDetail,
)
from .serializers import (
    RegistrationSerializer,
    ProfileSerializer,
    ProviderSerializer,
    ProductSerializer,
    ProviderProductSerializer,
    ProviderProductUpdateSerializer,
)


@api_view(['POST', ])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data['username'] = account.username
        data['response'] = 'Successfully registered'
        token=Token.objects.get(user=account).key
        data['token']=token
    else:
        data=serializer.errors
    return Response(data)


@api_view(['GET',])
def play_view(request):
    data={'1':'hello user'}
    return Response(data=data,status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def create_profile(request):
    user=request.user
    qs=Volunteer.objects.filter(user=user)
    if qs:
        return Response({'success':False,'exists':'Volunteer profile already exists for this user'})
    prof=Volunteer(user=user)
    serializer=ProfileSerializer(prof,data=request.data)
    data={}
    if serializer.is_valid():
        mail_id=serializer.validated_data['email']
        print(mail_id)
        _=send_conf_mail(request=request,email=mail_id)
        serializer.save()
        data['data']=serializer.data
        data['msg']='Please check your email for the verification code.'
    else:
        data=serializer.errors

    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
@vol_active
def create_provider(request):
    user=request.user
    vol=Volunteer.objects.get(user=user)
    serializer = ProviderSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        provider = serializer.save()
        data['success'] = True
        data['provider']=serializer.data
    else:
        data['success']=False
        data['errors']=serializer.errors
    return Response(data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated,])
@vol_active
def update_profile(request):
    """This view expects to receive all """
    user=request.user
    vol=Volunteer.objects.get(user=user)
    serializer=ProfileSerializer(vol,data=request.data,partial=True)
    data={}
    if serializer.is_valid():
        serializer.save()
        data['success']=True
        data['data']=serializer.data
    else:
        data['success']=False
        data['errors']=serializer.errors
    return Response(data=data)


@api_view(['POST'])
@permission_classes([IsAdminUser,])
@vol_active
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        _ = serializer.save()
        data['success'] = True
        data['product'] = serializer.data
    else:
        data['success'] = False
        data['errors'] = serializer.errors
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
@vol_active
def create_resource(request):
    serializer = ProviderProductSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        _ = serializer.save()
        data['success'] = True
        data['resource'] = serializer.data
    else:
        try:
            if serializer.errors.get('non_field_errors')[0].code=='unique':
                data['msg']='(Provider,Product) pair already present. Update the existing one instead'
                data['code']='unique'
        except Exception as e:
            print(e)
            pass
        data['success'] = False
        data['errors'] = serializer.errors
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
@vol_active
def update_resource(request):
    product_id=request.data.get('product')
    provider_id=request.data.get('provider')
    if product_id is None and provider_id is None:
        return Response(data={'success':False,'msg':'Resource ID not provided'},status=status.HTTP_406_NOT_ACCEPTABLE)
    try:
        resource=ProviderProductDetail.objects.get(provider=provider_id,product=product_id)
    except ProviderProductDetail.DoesNotExist:
        return Response(data={'success':False,'msg':'Resource does not exist'},status=status.HTTP_404_NOT_FOUND)

    data = {}
    serializer = ProviderProductUpdateSerializer(resource,data=request.data,partial=True)
    if serializer.is_valid():
        _ = serializer.save()
        data['success'] = True
        data['resource'] = serializer.data
    else:
        data['success'] = False
        data['errors'] = serializer.errors
    return Response(data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated,])
# @vol_active
# def create_delivery_executive(request):
#     serializer = ProductSerializer(data=request.data)
#     data = {}
#     if serializer.is_valid():
#         _ = serializer.save()
#         data['success'] = True
#         data['product'] = serializer.data
#     else:
#         data['success'] = False
#         data['errors'] = serializer.errors
#     return Response(data)


class ProviderListView(ListAPIView):
    # queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    authentication_classes = ()
    permission_classes=()
    pagination_class = PageNumberPagination
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ['pin_code','address','contact']
    ordering_fields = ('modified',)
    ordering = ('-modified',)

    def get_queryset(self):
        """Support for searching with pin_code, provider contact, provider address """
        qs=Provider.objects.all()
        params=self.request.query_params

        pin_code=params.get('pin_code')
        if pin_code and qs:
            qs=qs.filter(pin_code=pin_code)

        address=params.get('address')
        if address and qs:
            qs=qs.filter(address__icontains=address)

        contact = params.get('contact')
        if contact and qs:
            qs = qs.filter(contact=contact)

        return qs


class ResourcesListView(ListAPIView):
    # queryset = ProviderProductDetail.objects.all()
    serializer_class = ProviderProductSerializer
    authentication_classes = ()
    permission_classes=()
    pagination_class = PageNumberPagination
    filter_backends = (OrderingFilter,SearchFilter)
    search_fields=('=pin_code','=provider__contact','provider__address','product__product_details')
    ordering_fields=('total',)
    ordering=('-total',)

    def get_queryset(self):
        """Support for searching with pin_code, provider contact, provider address, product details"""
        qs=ProviderProductDetail.objects.all()
        params=self.request.query_params

        pin_code=params.get('pin_code')
        if pin_code and qs:
            qs=qs.filter(pin_code=pin_code)

        provider_contact=params.get('provider_contact')
        if provider_contact and qs:
            qs=qs.filter(provider__contact=provider_contact)

        provider_address = params.get('provider_address')
        if provider_address and qs:
            qs = qs.filter(provider__address__icontains=provider_address)

        product_details = params.get('product_details')
        if product_details and qs:
            qs = qs.filter(product__product_details=product_details)

        return qs


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        vol=Volunteer.objects.get(user=user)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist,Volunteer.DoesNotExist):
        user = None
        vol=None
    if vol is not None and account_activation_token.check_token(user, token):
        vol.is_active = True
        vol.save()
        # login(request, user)
        # return redirect('account:create_profile', slug=str(user.registration_no).lower())
        return HttpResponse('Account activated!')

    else:
        return HttpResponse('Activation link is invalid!')
