from django.db import models
from django.utils import timezone
from django.conf import settings

class Destination(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/')
    is_trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class TourPackage(models.Model):
    DURATION_CHOICES = [
        ('1-3', '1-3 Days'),
        ('4-7', '4-7 Days'),
        ('8-14', '8-14 Days'),
        ('15+', '15+ Days'),
    ]
    
    CATEGORY_CHOICES = [
        ('honeymoon', 'Honeymoon'),
        ('adventure', 'Adventure'),
        ('family', 'Family'),
        ('solo', 'Solo'),
        ('religious', 'Religious'),
    ]
    
    title = models.CharField(max_length=200)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='family')
    description = models.TextField()
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES)
    
    # Pricing fields
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Base price (kept for compatibility)
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_per_couple = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_per_group = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    emi_available = models.BooleanField(default=True)
    emi_per_month = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    image = models.ImageField(upload_to='packages/')
    is_featured = models.BooleanField(default=False)
    inclusions = models.TextField(help_text="Comma-separated list")
    exclusions = models.TextField(help_text="Comma-separated list")
    itinerary = models.TextField(help_text="Day-wise schedule")
    available_from = models.DateField()
    available_to = models.DateField()
    popularity_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def get_inclusions_list(self):
        return [item.strip() for item in self.inclusions.split(',') if item.strip()]
    
    def get_exclusions_list(self):
        return [item.strip() for item in self.exclusions.split(',') if item.strip()]
    
    class Meta:
        ordering = ['-popularity_score', '-created_at']

class PackageImage(models.Model):
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='package_gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.package.title} - Image {self.order}"

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'package']
    
    def __str__(self):
        return f"{self.user.username} - {self.package.title}"

class Banner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_image = models.ImageField(upload_to='testimonials/', blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField()
    package = models.ForeignKey(TourPackage, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.customer_name} - {self.rating} stars"
