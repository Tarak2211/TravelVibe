# TravelVibe Setup Guide

Complete setup instructions for the TravelVibe e-commerce platform.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment Variables
Copy the example environment file:
```bash
copy .env.example .env
```

Edit `.env` and add your email credentials (for OTP functionality):
```
SECRET_KEY=your-secret-key-here
DEBUG=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 3. Run Setup Script
```bash
python setup_project.py
```

This will:
- Create all database migrations
- Apply migrations to create tables
- Set up the database schema

### 4. Create Admin User
```bash
python create_admin.py
```

Default credentials:
- Username: `admin`
- Email: `admin@travelvibe.com`
- Password: `admin123`

### 5. Populate Sample Data (Optional)
```bash
python populate_sample_data.py
```

This adds:
- 6 trending destinations (Goa, Bali, Manali, Paris, Dubai, Maldives)
- 6 featured tour packages
- 3 promotional banners
- 6 customer testimonials

### 6. Run Development Server
```bash
python manage.py runserver
```

## Access URLs

- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **User Login**: http://127.0.0.1:8000/accounts/login/
- **User Registration**: http://127.0.0.1:8000/accounts/register/
- **User Profile**: http://127.0.0.1:8000/accounts/profile/

## Features Available

### Step 1: User Management ✅
- Registration with email and phone number
- OTP verification for email
- Login and logout
- Password reset via email
- User profile management

### Step 2: Homepage ✅
- Hero section with search bar
- Promotional banners
- Trending destinations
- Featured tour packages
- Customer testimonials
- Footer with contact info

## Admin Panel Features

Login to admin panel with the credentials above to:

1. **Manage Users**
   - View all registered users
   - Verify user accounts
   - Manage user permissions

2. **Manage Destinations**
   - Add new destinations
   - Mark destinations as trending
   - Upload destination images

3. **Manage Tour Packages**
   - Create new packages
   - Set categories (Honeymoon, Adventure, Family, Solo, Religious)
   - Set pricing and duration
   - Mark packages as featured
   - Add inclusions/exclusions
   - Create day-wise itinerary

4. **Manage Banners**
   - Create promotional banners
   - Set banner order
   - Activate/deactivate banners

5. **Manage Testimonials**
   - Add customer reviews
   - Set ratings (1-5 stars)
   - Mark testimonials as featured

## Troubleshooting

### Database Errors
If you encounter database errors:
```bash
# Delete the database
Remove-Item db.sqlite3 -Force

# Run setup again
python setup_project.py
```

### Email Not Sending
Make sure your `.env` file has correct email settings:
- For Gmail, use an App Password (not your regular password)
- Enable 2-factor authentication and generate an app password
- Update EMAIL_HOST_USER and EMAIL_HOST_PASSWORD

### Import Errors
Make sure Django is installed:
```bash
pip install Django
```

## Testing the Application

1. **Register a New User**
   - Go to http://127.0.0.1:8000/accounts/register/
   - Fill in the registration form
   - Check your email for OTP
   - Verify OTP to activate account

2. **Browse Homepage**
   - View trending destinations
   - Browse featured packages
   - Read customer testimonials
   - Use search bar to filter packages

3. **Admin Panel**
   - Login to admin panel
   - Add/edit destinations and packages
   - Manage banners and testimonials

## Next Steps

Steps 3-9 are ready to be implemented:
- Package catalog with filters
- Package detail pages
- Booking system
- Payment integration
- User dashboard
- Complete admin features

All database models are already created and ready!

## Support

For issues or questions, refer to:
- README.md for project overview
- IMPLEMENTATION_PLAN.md for feature details
- Django documentation: https://docs.djangoproject.com/
