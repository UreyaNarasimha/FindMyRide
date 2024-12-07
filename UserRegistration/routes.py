from django.urls import path
from UserRegistration import views

urlpatterns = [
    path('userregistration/',views.UserRegistration.as_view()),
    path('user/userregistration/<int:pk>',views.UserRegistrationDetail.as_view()),
]
