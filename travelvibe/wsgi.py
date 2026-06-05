import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelvibe.settings')

# Run migrations automatically on Vercel (serverless — no build step runs manage.py)
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
IS_VERCEL = str(BASE_DIR).startswith('/var/task')

if IS_VERCEL:
    import django
    django.setup()
    from django.core.management import call_command
    try:
        call_command('migrate', '--run-syncdb', verbosity=0)
    except Exception:
        pass  # Don't crash the app if migrate fails

application = get_wsgi_application()
