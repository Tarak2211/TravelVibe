from django.contrib import admin
from .models import Destination, TourPackage, PackageImage, Wishlist, Banner, Testimonial

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'is_trending', 'created_at']
    list_filter = ['is_trending', 'country']
    search_fields = ['name', 'country']

@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ['title', 'destination', 'category', 'price', 'duration', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'category', 'duration', 'destination']
    search_fields = ['title', 'description']

@admin.register(PackageImage)
class PackageImageAdmin(admin.ModelAdmin):
    list_display = ['package', 'caption', 'order']
    list_filter = ['package']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'package', 'created_at']
    list_filter = ['created_at']

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order']
    list_filter = ['is_active']
    ordering = ['order']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'rating', 'package', 'is_featured', 'created_at']
    list_filter = ['rating', 'is_featured']
    search_fields = ['customer_name', 'review']
