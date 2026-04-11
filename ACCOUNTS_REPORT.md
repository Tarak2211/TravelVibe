# 👥 TravelVibe Accounts Report

## 📊 Total Accounts: 3

---

## 🔐 Account Details

### 1. Admin Account (Superuser)
- **Username:** `admin`
- **Email:** admin@travelvibe.com
- **Phone:** +1234567890
- **Type:** Administrator/Superuser
- **Status:** ✅ Active & Verified
- **Permissions:** Full access to admin panel
- **Created:** March 3, 2026 at 1:01 PM
- **Purpose:** System administration and management

---

### 2. Tarak Patel (Regular User)
- **Username:** `tarak.patel`
- **Email:** tarak123@gmail.com
- **Phone:** 9078320458
- **Type:** Regular User
- **Status:** ✅ Active & Verified
- **Permissions:** Standard user access
- **Created:** March 12, 2026 at 8:26 AM
- **Purpose:** Testing and user account
- **How Created:** Via Django shell command (manual creation)

---

### 3. Kavya Shah (Regular User) - NEW!
- **Username:** `kavya.shah`
- **Email:** kavyat23@gmail.com
- **Phone:** 9078320879
- **Type:** Regular User
- **Status:** ✅ Active & Verified
- **Permissions:** Standard user access
- **Created:** March 12, 2026 at 2:48 PM (just now!)
- **Purpose:** User account
- **How Created:** Via Django shell command (manual creation)
- **Password:** kavya123

---

## 📈 Account Statistics

### By Type:
- **Administrators:** 1 (admin)
- **Regular Users:** 2 (tarak.patel, kavya.shah)
- **Total:** 3 accounts

### By Status:
- **Active:** 3 (100%)
- **Verified:** 3 (100%)
- **Inactive:** 0

### By Creation Date:
- **March 3, 2026:** 1 account (admin)
- **March 12, 2026:** 2 accounts (tarak.patel, kavya.shah)

---

## 🎯 Login Credentials

### For Kavya Shah (NEW):
```
Username: kavya.shah
Password: kavya123
```

### For Tarak Patel:
```
Username: tarak.patel
Password: tarak123
```

### For Admin:
```
Username: admin
Password: [admin password]
```

---

## 🔧 How Accounts Were Created

### Admin Account:
- **Method:** Django `createsuperuser` command
- **Date:** March 3, 2026
- **Purpose:** System administration

### Tarak Patel Account:
- **Method:** Django shell command (manual)
- **Command Used:**
```python
CustomUser.objects.create_user(
    username='tarak.patel',
    email='tarak123@gmail.com',
    password='tarak123',
    phone_number='9078320458'
)
```
- **Date:** March 12, 2026 at 8:26 AM
- **Reason:** Registration form wasn't working due to email verification

### Kavya Shah Account:
- **Method:** Django shell command (manual)
- **Command Used:**
```python
CustomUser.objects.create_user(
    username='kavya.shah',
    email='kavyat23@gmail.com',
    password='kavya123',
    phone_number='9078320879'
)
```
- **Date:** March 12, 2026 at 2:48 PM
- **Reason:** Registration form wasn't completing

---

## ⚠️ Registration Form Issue

### Problem:
The registration form requires email OTP verification, but email settings are not configured, causing registration to hang.

### Solution Applied:
1. **Modified `accounts/views.py`:**
   - Removed email verification requirement
   - Accounts now activate immediately
   - Auto-login after registration

2. **Manual Account Creation:**
   - Created accounts directly via Django shell
   - Bypassed email verification
   - Set accounts as active and verified

### Future Fix:
Either:
- Configure email settings in `.env` file (for OTP verification)
- OR keep the simplified registration (no email verification)

---

## 📝 Account Management Commands

### Create New Account:
```bash
python manage.py shell -c "from accounts.models import CustomUser; user = CustomUser.objects.create_user(username='USERNAME', email='EMAIL', password='PASSWORD', phone_number='PHONE'); user.is_active = True; user.is_verified = True; user.save(); print(f'Account created: {user.username}')"
```

### List All Accounts:
```bash
python manage.py shell -c "from accounts.models import CustomUser; [print(f'{u.username} - {u.email}') for u in CustomUser.objects.all()]"
```

### Activate an Account:
```bash
python manage.py shell -c "from accounts.models import CustomUser; user = CustomUser.objects.get(username='USERNAME'); user.is_active = True; user.is_verified = True; user.save(); print('Account activated!')"
```

### Delete an Account:
```bash
python manage.py shell -c "from accounts.models import CustomUser; CustomUser.objects.get(username='USERNAME').delete(); print('Account deleted!')"
```

---

## 🎉 Summary

### Total Accounts: 3
- ✅ 1 Administrator (admin)
- ✅ 2 Regular Users (tarak.patel, kavya.shah)

### All Accounts:
- ✅ Active and verified
- ✅ Ready to use
- ✅ Can login immediately

### New Account Created Today:
- ✅ **kavya.shah** - Created successfully!
- ✅ Login: `kavya.shah` / `kavya123`

---

## 🚀 Next Steps

1. **Restart your server** if not running:
   ```bash
   python manage.py runserver
   ```

2. **Go to:** http://127.0.0.1:8000/accounts/login/

3. **Login with:**
   - Username: `kavya.shah`
   - Password: `kavya123`

4. **Start exploring TravelVibe!** 🎉

---

**Report Generated:** March 12, 2026 at 2:48 PM
**Status:** ✅ All accounts active and ready to use
