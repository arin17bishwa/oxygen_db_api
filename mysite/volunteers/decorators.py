from .models import Volunteer
from rest_framework.response import Response
from rest_framework import status


def vol_active(function):
    def wrapper(request,*args,**kwargs):
        user=request.user
        vol=Volunteer.objects.filter(user=user)
        if len(vol)<1:
            return Response({'error':'No profile created'},status=status.HTTP_401_UNAUTHORIZED)
        vol=vol[0]
        if not vol.is_active:
            return Response({'error':'Profile not confirmed'},status=status.HTTP_403_FORBIDDEN)
        return function(request,*args,**kwargs)

    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper
