from django.db import models

class RiderRegistrationModel(models.Model):
    id = models.AutoField(primary_key=True)
    rider_name = models.CharField(max_length=255)
    email_id = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=10)
    student_id =models.CharField(max_length=255)
    university_name = models.CharField(max_length=255)
    drivers_license_id = models.CharField(max_length=255)
    address = models.TextField()
    zipcode = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

