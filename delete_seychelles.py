"""
Delete Seychelles destination and packages
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelvibe.settings')
django.setup()

from store.models import Destination, TourPackage

def delete_seychelles():
    print("Deleting Seychelles...")
    
    # Delete Seychelles destination (this will also delete related packages due to CASCADE)
    deleted_count = Destination.objects.filter(name="Seychelles").delete()
    
    print(f"✅ Deleted: {deleted_count}")
    print(f"\nRemaining Destinations: {Destination.objects.count()}")
    print(f"Remaining Packages: {TourPackage.objects.count()}")

if __name__ == "__main__":
    delete_seychelles()
