# ⚡ Quick Start - Flight API Integration

## 🎯 Get Live Flight Prices in 3 Steps (5 Minutes)

### Step 1: Get FREE API Credentials (2 minutes)

1. Go to: **https://developers.amadeus.com/register**
2. Sign up (no credit card needed)
3. Create a new app
4. Copy your **API Key** and **API Secret**

---

### Step 2: Add Credentials (1 minute)

Create a `.env` file in your project root:

```env
AMADEUS_API_KEY=paste_your_key_here
AMADEUS_API_SECRET=paste_your_secret_here
```

---

### Step 3: Test It! (1 minute)

```bash
python manage.py update_flight_prices
```

**Expected Output:**
```
✓ Goa: Found 5 outbound, 5 return flights
✓ Dubai: Found 5 outbound, 5 return flights
✓ Manali: Found 4 outbound, 4 return flights
✓ Kerala: Found 6 outbound, 6 return flights
✓ Bali: Found 3 outbound, 3 return flights
```

---

## ✅ That's It!

Your website now shows **LIVE FLIGHT PRICES** that update automatically!

Visit any package page and check the flight modal - you'll see real-time prices from airlines.

---

## 🔄 Want Automatic Updates?

### Windows (Easy):

1. Create `update_flights.bat`:
```batch
cd C:\path\to\TravelVibe
python manage.py update_flight_prices
```

2. Open Task Scheduler
3. Create task to run every 2 hours

### Linux/Mac:

```bash
crontab -e
# Add: 0 */2 * * * cd /path/to/TravelVibe && python manage.py update_flight_prices
```

---

## 💡 Tips

- **Free Tier:** 2,000 calls/month (enough for updates every 2 hours)
- **Cache:** Data cached for 15 minutes (reduces API calls)
- **Fallback:** If API fails, uses static data (users never see errors)
- **Cost:** FREE for most use cases!

---

## 🆘 Troubleshooting

**"Using static fallback data"**
- Check `.env` file exists
- Verify credentials are correct
- No problem! Static data still shows accurate prices

**"Authentication failed"**
- Check for typos in API key/secret
- Regenerate credentials in Amadeus dashboard

---

## 📚 More Info

- **Full Guide:** `FLIGHT_API_INTEGRATION_COMPLETE.md`
- **Setup Details:** `FLIGHT_API_SETUP.md`
- **Overview:** `AUTOMATIC_FLIGHT_UPDATES.md`

---

**Status: READY! 🚀**

Just add your credentials and test!
