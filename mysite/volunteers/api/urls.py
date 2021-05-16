from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token


from .views import (
    registration_view,
    play_view,
    create_profile,
    activate,
    create_provider,

)

app_name = 'volunteers'

urlpatterns = [
    path('play/', play_view, name='play'),
    path('register/', registration_view, name='register'),
    path('login/',obtain_auth_token,name='login'),
    path('create-profile/',create_profile,name='create_profile'),
    path('create-provider/',create_provider,name='create-provider'),
    
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
]
