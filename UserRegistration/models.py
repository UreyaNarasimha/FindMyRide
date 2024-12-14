from django.db import models
from django.contrib.auth.models import AbstractUser

class UserRegistrationModel(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255,blank=True,unique=True)
    email = models.EmailField(unique=True,blank=True)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=10)
    student_id =models.CharField(max_length=255)
    university_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

