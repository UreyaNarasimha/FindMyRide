from django.urls import path
from RiderAuthentication import views

urlpatterns = [
    path('login/',views.RiderLogin.as_view()),
    path('logout/',views.RiderLogout.as_view()),
]