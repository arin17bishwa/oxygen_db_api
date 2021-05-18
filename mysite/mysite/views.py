from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


# Create your views here.

@api_view(['GET',])
def home_view(request):
    data = {
        'api info': 'https://docs.google.com/spreadsheets/d/1lhOzLQC2xLgiry_8iW9cDtWCh75m-VJx_blKkekQAZQ/edit?usp'
                    '=sharing',
        'msg': 'Be good people'
    }
    return Response(data=data,status=status.HTTP_200_OK)
