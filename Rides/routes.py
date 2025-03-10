from django.urls import path
from Rides import views

urlpatterns = [
    path('avaliableriders/',views.AvaliableRiders.as_view()),
    path('booking/',views.RideBookings.as_view()),
    path('ridecompletion/<int:pk>',views.UpdateRiderStatus.as_view()),
    path('csv/',views.CSVFileGenerator.as_view()),
    path('bookings/user',views.UserBookings.as_view()),
    path('bookings/rider',views.RiderBookings.as_view()),
    path('bookings/<int:pk>',views.SpeficRideBookingDetails.as_view())
]