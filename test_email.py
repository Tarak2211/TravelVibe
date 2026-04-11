"""
Run this to test if email is working:
  python test_email.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelvibe.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print(f"EMAIL_HOST_USER : {settings.EMAIL_HOST_USER}")
print(f"EMAIL_HOST      : {settings.EMAIL_HOST}")
print(f"EMAIL_PORT      : {settings.EMAIL_PORT}")
print(f"PASSWORD set    : {'YES' if settings.EMAIL_HOST_PASSWORD else 'NO'}")
print(f"PASSWORD length : {len(settings.EMAIL_HOST_PASSWORD)}")
print()

try:
    send_mail(
        subject='TravelVibe — Email Test',
        message='If you see this, email is working correctly!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.EMAIL_HOST_USER],
        fail_silently=False,
    )
    print("SUCCESS — Email sent! Check your inbox.")
except Exception as e:
    print(f"FAILED — {e}")
