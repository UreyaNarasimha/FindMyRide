from django.db import models

class RideBookings(models.Model):
    booking_id = models.AutoField(primary_key=True)
    rider_id = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    pickup_address = models.TextField()
    pickup_zipcode = models.CharField(max_length=255)
    destination = models.TextField()
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

