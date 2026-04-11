# ✅ User Bookings Created Successfully!

## 🎉 What I've Done

I've created sample bookings for your users so you can see the booking details when you login!

---

## 📋 Bookings Created

### 1. Bhargav Ramani - Dubai Package
- **Booking ID:** TVB15FC288
- **Package:** Dubai Desert Safari & City Tour
- **Destination:** Dubai, UAE
- **Travel Date:** March 27, 2026 (15 days from now)
- **Travelers:** 2 Adults
  - Bhargav Ramani (28 years, Male)
  - Priya Ramani (26 years, Female)
- **Flight:** Air India AI 995
  - Departure: 02:00 AM from Delhi (DEL)
  - Arrival: 04:30 AM in Dubai (DXB)
  - Duration: 3h 30m
  - Class: Economy
- **Pricing:**
  - Base Fare: ₹89,998
  - Taxes & Fees: ₹8,999.80
  - Total: ₹98,997.80
- **Status:** ✅ Confirmed

---

### 2. Dhruv Patel - Goa Package
- **Booking ID:** TVE321AB4B
- **Package:** Goa Beach Paradise
- **Destination:** Goa, India
- **Travel Date:** March 22, 2026 (10 days from now)
- **Travelers:** 1 Adult
  - Dhruv Patel (25 years, Male)
- **Flight:** Air India AI 804
  - Departure: 06:00 AM from Delhi (DEL)
  - Arrival: 08:30 AM in Goa (GOI)
  - Duration: 2h 30m
  - Class: Economy
- **Pricing:**
  - Base Fare: ₹24,999
  - Taxes & Fees: ₹2,499.90
  - Total: ₹27,498.90
- **Status:** ✅ Confirmed

---

### 3. Het Patel - Bali Package
- **Booking ID:** TVA45CFD92
- **Package:** Bali Island Paradise
- **Destination:** Bali, Indonesia
- **Travel Date:** April 1, 2026 (20 days from now)
- **Travelers:** 2 Adults + 1 Child
  - Het Patel (30 years, Male)
  - Riya Patel (28 years, Female)
  - Aarav Patel (5 years, Male)
- **Flight:** Air India AI 336
  - Departure: 11:30 PM from Delhi (DEL)
  - Arrival: 12:45 PM+1 in Denpasar (DPS)
  - Duration: 13h 15m
  - Stops: 1 Stop (Singapore - 2h 30m layover)
  - Class: Economy
- **Pricing:**
  - Base Fare: ₹149,997
  - Taxes & Fees: ₹14,999.70
  - Total: ₹164,996.70
- **Status:** ✅ Confirmed

---

## 🔐 Login Credentials to Test

### Bhargav Ramani:
```
Username: bhargav.ramani
Password: bhargav123
```
**What you'll see:**
- Dubai package booking
- Flight: AI 995 at 02:00 AM to Dubai
- 2 travelers
- Total: ₹98,997.80

---

### Dhruv Patel:
```
Username: dhruv.patel
Password: dhruv123
```
**What you'll see:**
- Goa package booking
- Flight: AI 804 at 06:00 AM to Goa
- 1 traveler
- Total: ₹27,498.90

---

### Het Patel:
```
Username: het.patel
Password: het123
```
**What you'll see:**
- Bali package booking
- Flight: AI 336 at 11:30 PM to Bali
- 3 travelers (2 adults + 1 child)
- Total: ₹164,996.70

---

## 🎯 How to View Bookings

### Step 1: Login
1. Go to: http://127.0.0.1:8000/accounts/login/
2. Use any of the credentials above
3. Click Login

### Step 2: View Profile
- After login, click **"Profile"** in the navigation menu
- OR go directly to: http://127.0.0.1:8000/accounts/profile/

### Step 3: See Your Bookings
You'll see:
- ✈️ Booking ID and status
- 📦 Package details with image
- 📅 Travel date
- 👥 Number of travelers
- ✈️ Complete flight information:
  - Departure time and airport
  - Arrival time and airport
  - Airline and flight number
  - Duration and stops
  - Seat class
- 👥 List of all travelers
- 💰 Complete pricing breakdown

---

## 📊 Summary

### Total Bookings Created: 3

1. **Bhargav Ramani** → Dubai (₹98,997.80)
2. **Dhruv Patel** → Goa (₹27,498.90)
3. **Het Patel** → Bali (₹164,996.70)

### Total Revenue: ₹291,493.40

---

## ✨ Features in Profile Page

### Booking Card Shows:
- ✅ Booking ID with status badge
- ✅ Package image and title
- ✅ Destination name
- ✅ Travel date
- ✅ Number of adults and children
- ✅ Complete flight details:
  - Departure time and location
  - Arrival time and location
  - Airline name
  - Flight number
  - Duration
  - Stops/layovers
  - Seat class
- ✅ List of all travelers with age and gender
- ✅ Pricing breakdown:
  - Base fare
  - Taxes & fees
  - Discounts (if any)
  - Total amount

---

## 🎯 What to Do Now

1. **Login with Bhargav's account:**
   ```
   Username: bhargav.ramani
   Password: bhargav123
   ```

2. **Click "Profile" in navigation**

3. **See his Dubai booking with all details!**

---

## 💡 Adding More Bookings

To create more bookings for testing, run:

```bash
python manage.py shell
```

Then:
```python
from accounts.models import CustomUser
from store.models import TourPackage
from bookings.models import Booking, Traveler
from datetime import date, timedelta
from decimal import Decimal

# Get user and package
user = CustomUser.objects.get(username='USERNAME')
package = TourPackage.objects.filter(destination__name='DESTINATION').first()

# Create booking
booking = Booking.objects.create(
    user=user,
    package=package,
    travel_date=date.today() + timedelta(days=15),
    adults_count=2,
    children_count=0,
    base_fare=Decimal('50000'),
    tax_amount=Decimal('5000'),
    total_amount=Decimal('55000'),
    status='confirmed'
)

# Add travelers
Traveler.objects.create(booking=booking, name='Name 1', age=30, gender='M')
Traveler.objects.create(booking=booking, name='Name 2', age=28, gender='F')

print(f'Booking created: {booking.booking_id}')
```

---

**Status:** ✅ COMPLETE

**Next Action:** Login with bhargav.ramani and check the Profile page!

**Date:** March 12, 2026
