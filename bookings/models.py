from django.db import models
from django.conf import settings
from store.models import TourPackage
import uuid


def _send_notifications_async(booking_id):
    """Send notifications after booking is saved (called via post-save signal)."""
    pass  # handled by signal below

class SavedTraveler(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_travelers')
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    usage_limit = models.IntegerField(default=1)
    used_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.code
    
    def is_valid(self):
        from django.utils import timezone
        return (self.is_active and 
                self.valid_from <= timezone.now() <= self.valid_to and
                self.used_count < self.usage_limit)

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial Payment'),
        ('paid', 'Fully Paid'),
        ('refunded', 'Refunded'),
    ]

    booking_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    travel_date = models.DateField()
    adults_count = models.IntegerField(default=1)
    children_count = models.IntegerField(default=0)
    base_fare = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Payment tracking
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Amount paid so far")
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Balance due")
    remaining_due_date = models.DateField(null=True, blank=True, help_text="Date by which remaining payment must be made")
    payment_notes = models.TextField(blank=True, default='', help_text="Any notes about payment arrangement")

    # Flight details — Outbound
    outbound_airline = models.CharField(max_length=100, blank=True, default='')
    outbound_flight_no = models.CharField(max_length=20, blank=True, default='')
    outbound_departure = models.CharField(max_length=20, blank=True, default='')
    outbound_arrival = models.CharField(max_length=20, blank=True, default='')
    outbound_duration = models.CharField(max_length=20, blank=True, default='')
    outbound_stops = models.CharField(max_length=100, blank=True, default='Direct')
    outbound_from = models.CharField(max_length=50, blank=True, default='')
    outbound_to = models.CharField(max_length=50, blank=True, default='')

    # Flight details — Return
    return_airline = models.CharField(max_length=100, blank=True, default='')
    return_flight_no = models.CharField(max_length=20, blank=True, default='')
    return_departure = models.CharField(max_length=20, blank=True, default='')
    return_arrival = models.CharField(max_length=20, blank=True, default='')
    return_duration = models.CharField(max_length=20, blank=True, default='')
    return_stops = models.CharField(max_length=100, blank=True, default='Direct')
    return_from = models.CharField(max_length=50, blank=True, default='')
    return_to = models.CharField(max_length=50, blank=True, default='')
    seat_class = models.CharField(max_length=20, blank=True, default='Economy')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = f"TV{uuid.uuid4().hex[:8].upper()}"
        # Auto-calculate remaining
        self.remaining_amount = self.total_amount - self.amount_paid
        # Auto-set payment status
        if self.amount_paid <= 0:
            self.payment_status = 'unpaid'
        elif self.remaining_amount <= 0:
            self.payment_status = 'paid'
        else:
            self.payment_status = 'partial'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_id} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']


class Traveler(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='travelers')
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    def __str__(self):
        return f"{self.name} - {self.booking.booking_id}"

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('upi', 'UPI'),
        ('card', 'Credit/Debit Card'),
        ('netbanking', 'Net Banking'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_TYPE_CHOICES = [
        ('full', 'Full Payment'),
        ('partial', 'Partial Payment'),
    ]
    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES, default='full')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.transaction_id} - {self.booking.booking_id}"

class Inquiry(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    package = models.ForeignKey(TourPackage, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.email}"
    
    class Meta:
        verbose_name_plural = 'Inquiries'
        ordering = ['-created_at']
