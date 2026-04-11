@echo off
echo ========================================
echo  TravelVibe Flight API Setup
echo ========================================
echo.

echo Step 1: Installing required packages...
pip install requests python-dotenv celery redis

echo.
echo Step 2: Creating .env file...
if not exist .env (
    echo # Amadeus Flight API Credentials > .env
    echo AMADEUS_API_KEY=your_api_key_here >> .env
    echo AMADEUS_API_SECRET=your_api_secret_here >> .env
    echo.
    echo ✓ .env file created!
    echo.
    echo IMPORTANT: Edit .env file and add your Amadeus API credentials
    echo Get them from: https://developers.amadeus.com/register
) else (
    echo .env file already exists
)

echo.
echo Step 3: Testing flight API...
python manage.py update_flight_prices

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Get FREE API credentials from: https://developers.amadeus.com/register
echo 2. Edit .env file with your credentials
echo 3. Run: python manage.py update_flight_prices
echo 4. Set up automatic updates (see FLIGHT_API_SETUP.md)
echo.
pause
