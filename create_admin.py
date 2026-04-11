"""
Create default admin user for TravelVibe
Run after migrations: python create_admin.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelvibe.settings')
django.setup()

from accounts.models import CustomUser

def create_admin():
    username = "admin"
    email = "admin@travelvibe.com"
    password = "admin123"
    
    if CustomUser.objects.filter(username=username).exists():
        print(f"⚠️  Admin user '{username}' already exists!")
        admin = CustomUser.objects.get(username=username)
        print(f"\nExisting admin details:")
        print(f"Username: {admin.username}")
        print(f"Email: {admin.email}")
        return
    
    admin = CustomUser.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        phone_number="+1234567890",
        is_verified=True
    )
    
    print("✅ Admin user created successfully!")
    print("\n" + "="*50)
    print("ADMIN LOGIN CREDENTIALS")
    print("="*50)
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print("="*50)
    print("\nLogin URLs:")
    print("- Admin Panel: http://127.0.0.1:8000/admin/")
    print("- User Login: http://127.0.0.1:8000/accounts/login/")
    print("\n⚠️  IMPORTANT: Change this password in production!")

if __name__ == "__main__":
    create_admin()
