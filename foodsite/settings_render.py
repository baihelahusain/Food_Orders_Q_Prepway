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
        
        # Make sure SSL is properly configured
        db_config['OPTIONS'] = {
            'sslmode': 'require',
        }
        
        # Don't keep connections open too long
        db_config['CONN_MAX_AGE'] = 0
        
        # Add connection health checks
        db_config['CONN_HEALTH_CHECKS'] = True
        
        DATABASES = {
            'default': db_config
        }
        
        # Test the connection
        try:
            import psycopg2
            conn = psycopg2.connect(DATABASE_URL)
            conn.close()
            print("✅ Successfully tested direct connection to PostgreSQL")
        except Exception as e:
            print(f"⚠️ Direct connection test failed: {e}")
        
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