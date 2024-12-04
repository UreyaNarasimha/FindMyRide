from django.db import models

class AvaliableRidersModel(models.Model):
    avaliableriderslist_id = models.AutoField(primary_key=True)
    riders_details = models.JSONField(default={})
    user_id = models.CharField(max_length=255)
    pickup_address = models.TextField()
    pickup_zipcode = models.CharField(max_length=255)
    destination = models.TextField()
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class RideBookingModel(models.Model):
    Booking_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=255)
    rider_id = models.CharField(max_length=255)
    pickup_address = models.TextField()
    pickup_zipcode = models.CharField(max_length=255)
    destination = models.TextField()
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BookingLogs(models.Model):
    Booking_log_id = models.AutoField(primary_key=True)
    booking_id = models.CharField(max_length=255)
    booking_details = models.JSONField()

class AvaliableRidersLogs(models.Model):
    avaliableriders_log_id = models.AutoField(primary_key=True)
    avaliableriders_details = models.JSONField()