from django.urls import path
from RiderRegistration import views

urlpatterns = [
    path('riderregistration/',views.RiderRegistration.as_view()),
    path('riderregistration/<int:pk>',views.RiderRegistrationDetail.as_view()),
]