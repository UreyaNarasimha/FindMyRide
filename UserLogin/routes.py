from django.urls import path
from UserLogin import views

urlpatterns = [
    path('login/',views.UserLogin.as_view()),
    path('logout/',views.UserLogout.as_view()),
    path('captcha/',views.Captcha.as_view()),
    path('sendotp/',views.OTPGenerator.as_view()),
    path('verifyotp/',views.OTPVerification.as_view())
]