# TravelVibe - Quick Start Guide

## ✨ Beautiful, Modern Design!

TravelVibe features a **stunning professional UI** with:
- 🎨 Gorgeous purple-violet gradient color scheme
- ✨ Smooth animations and transitions
- 💎 Glassmorphism effects
- 🌈 Modern card designs with hover effects
- 📱 Fully responsive for all devices

Get TravelVibe running in 5 minutes!

## Prerequisites

- Python 3.8 or higher installed
- pip (Python package manager)

## Installation Steps

### 1. Install Dependencies (1 minute)
```bash
pip install -r requirements.txt
```

### 2. Setup Database (1 minute)
```bash
python setup_project.py
```

### 3. Create Admin User (30 seconds)
```bash
python create_admin.py
```

**Admin Credentials:**
- Username: `admin`
- Password: `admin123`

### 4. Add Sample Data - Optional (30 seconds)
```bash
python populate_sample_data.py
```

This adds:
- 6 destinations (Goa, Bali, Manali, Paris, Dubai, Maldives)
- 6 tour packages
- 3 promotional banners
- 6 customer testimonials

### 5. Run Server (10 seconds)
```bash
python manage.py runserver
```

## Access the Application

Open your browser and visit:

- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Register**: http://127.0.0.1:8000/accounts/register/
- **Login**: http://127.0.0.1:8000/accounts/login/

## Test the Features

### 1. Test User Registration
1. Go to http://127.0.0.1:8000/accounts/register/
2. Fill in the form
3. Check your email for OTP (if email is configured)
4. Verify OTP to activate account

### 2. Test Admin Panel
1. Go to http://127.0.0.1:8000/admin/
2. Login with `admin` / `admin123`
3. Explore:
   - Users management
   - Destinations
   - Tour Packages
   - Banners
   - Testimonials

### 3. Browse Homepage
1. Go to http://127.0.0.1:8000/
2. See trending destinations
3. Browse featured packages
4. Read customer testimonials
5. Try the search bar

## Email Configuration (Optional)

To enable OTP emails, create a `.env` file:

```
SECRET_KEY=your-secret-key
DEBUG=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

For Gmail:
1. Enable 2-factor authentication
2. Generate an App Password
3. Use the app password in EMAIL_HOST_PASSWORD

## Troubleshooting

### Database Locked Error
```bash
# Close all Python processes, then:
Remove-Item db.sqlite3 -Force
python setup_project.py
```

### Import Errors
```bash
pip install Django python-decouple Pillow reportlab
```

### Port Already in Use
```bash
python manage.py runserver 8001
```

## What's Working

✅ User registration with OTP verification
✅ Login and logout
✅ Password reset via email
✅ User profile management
✅ Homepage with search
✅ Trending destinations display
✅ Featured packages display
✅ Customer testimonials
✅ Admin panel for content management

## Next Steps

The foundation is complete! Steps 3-9 database models are ready:
- Package catalog with filters
- Package detail pages
- Booking system
- Payment processing
- User dashboard
- Complete admin features

## Need Help?

Check these files:
- `README.md` - Full project documentation
- `SETUP_GUIDE.md` - Detailed setup instructions
- `PROJECT_STATUS.md` - Current project status

## Summary

You now have a working Django e-commerce platform for travel bookings with:
- Complete user authentication system
- Beautiful homepage with search
- Admin panel for content management
- Database ready for booking features

Happy coding! 🚀
