# TravelVibe E-Commerce Website

A comprehensive Django-based e-commerce platform for travel packages and tour bookings.4

---

## Project Structure

```
TravelVibe/
├── manage.py
├── requirements.txt
├── travelvibe/              # Main project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── accounts/                # User Management (Step 1)
│   ├── models.py            # CustomUser, OTPVerification
│   ├── views.py             # Registration, Login, Profile
│   ├── forms.py             # User forms
│   └── utils.py             # OTP utilities
├── store/                   # Homepage & Packages (Steps 2-4)
│   ├── models.py            # Destination, TourPackage, Wishlist, Banner, Testimonial
│   ├── views.py             # Homepage, Package catalog, Package detail
│   └── admin.py             # Admin interfaces
└── bookings/                # Booking System (Steps 5-7)
    ├── models.py            # Booking, Traveler, Payment, Coupon, Inquiry
    ├── views.py             # Booking process, Checkout, User dashboard
    └── admin.py             # Booking management
```

---
