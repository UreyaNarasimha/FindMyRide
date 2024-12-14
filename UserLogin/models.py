from django.db import models

# Create your models here.
class OTP(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=255)
    otp = models.CharField(max_length=255)
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
