from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    passport_expiry = models.DateField(blank=True, null=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    address = models.TextField(blank=True, default='')
    aadhar_number = models.CharField(max_length=12, blank=True, default='')
    
    def __str__(self):
        return self.email

class OTPVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    def is_valid(self):
        return not self.is_used and (timezone.now() - self.created_at) < timedelta(minutes=10)
    
    def __str__(self):
        return f"OTP for {self.user.email}"
