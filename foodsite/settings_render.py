"""
Django settings for foodsite project on Render.

These settings extend the base settings with Render-specific configurations.
"""

from .settings import *  # Import all settings from the base settings file
import os

# Override settings for Render deployment
DEBUG = False

# Explicit allowed hosts for Render
ALLOWED_HOSTS = ['food-orders-q-prepway.onrender.com', '.onrender.com', 'localhost', '127.0.0.1']

# Security settings for production
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_REFERRER_POLICY = "same-origin"

# CORS settings
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://food-orders-q-prepway.onrender.com",
]

# Make sure staticfiles directory exists
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
os.makedirs(STATIC_ROOT, exist_ok=True)

# Database settings for Supabase PostgreSQL
import dj_database_url

# Print all environment variables for debugging (masking sensitive values)
for key, value in os.environ.items():
    if 'SECRET' in key or 'PASSWORD' in key or 'KEY' in key:
        print(f"ENV: {key}=***")
    else:
        print(f"ENV: {key}={value}")

DATABASE_URL = os.environ.get('DATABASE_URL')

print(f"DATABASE_URL in settings: {'Set' if DATABASE_URL else 'Not set'}")

# Try to use DATABASE_URL if provided
if DATABASE_URL:
    try:
        # For using with Supabase, need to disable prepared statements
        db_config = dj_database_url.parse(DATABASE_URL)
        
        # Check if using connection pooler
        is_pooler = 'pooler.supabase.com' in db_config.get('HOST', '')
        
        # Configure based on connection type
        if is_pooler:
            print("Using Supabase connection pooler (IPv4 compatible)")
            # For pooler, need these specific settings
            db_config['OPTIONS'] = {
                'sslmode': 'require',
            }
            # For transaction pooler mode, disable prepared statements
            if ':6543/' in DATABASE_URL:
                print("Using transaction pooler mode - disabling prepared statements")
                db_config['OPTIONS']['options'] = '-c statement_timeout=30000 -c idle_in_transaction_session_timeout=30000'
                db_config['DISABLE_SERVER_SIDE_CURSORS'] = True
                db_config['CONN_MAX_AGE'] = 0
        else:
            # Direct connection settings
            print("Using direct database connection (requires IPv6)")
            db_config['OPTIONS'] = {
                'sslmode': 'require',
            }
        
        # Add connection health checks
        db_config['CONN_HEALTH_CHECKS'] = True
        
        DATABASES = {
            'default': db_config
        }
        
        # Print configuration for debugging
        print(f"Database config: HOST={db_config.get('HOST')}, NAME={db_config.get('NAME')}, ENGINE={db_config.get('ENGINE')}")
    except Exception as e:
        print(f"❌ Error configuring PostgreSQL: {e}")
        print("Falling back to SQLite")
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }
else:
    print("WARNING: No DATABASE_URL found. Using SQLite database.")
    # Fall back to SQLite for local development
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    } 