from django.urls import path
from RiderAuthentication import viewssss

urlpatterns = [
    path('rides/login/',viewssss.RiderLogin.as_view()),
    path('rider/logout/',viewssss.RiderLogout.as_view()),
]