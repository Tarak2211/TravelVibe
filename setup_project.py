"""
Complete setup script for TravelVibe project
Run this after installing requirements: python setup_project.py
"""
import os
import sys
import subprocess

print("="*60)
print("TRAVELVIBE PROJECT SETUP")
print("="*60)

# Step 1: Run migrations
print("\n1. Creating database migrations...")
result = subprocess.run(['python', 'manage.py', 'makemigrations'], 
                       capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print("Error:", result.stderr)
    sys.exit(1)

print("\n2. Applying migrations...")
result = subprocess.run(['python', 'manage.py', 'migrate'], 
                       capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print("Error:", result.stderr)
    sys.exit(1)

print("\n" + "="*60)
print("✅ PROJECT SETUP COMPLETE!")
print("="*60)
print("\nNext steps:")
print("1. Create admin user: python create_admin.py")
print("2. Add sample data: python populate_sample_data.py")
print("3. Run server: python manage.py runserver")
print("\nAccess URLs:")
print("- Homepage: http://127.0.0.1:8000/")
print("- Admin: http://127.0.0.1:8000/admin/")
print("- Login: http://127.0.0.1:8000/accounts/login/")
print("- Register: http://127.0.0.1:8000/accounts/register/")
