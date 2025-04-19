"""
Django settings for foodsite project on Render.

These settings extend the base settings with Render-specific configurations.
"""

from .settings import *  # Import all settings from the base settings file

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
    "https://food-orders-q-prepway.onrender.com",
]

# Make sure staticfiles directory exists
import os
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
os.makedirs(STATIC_ROOT, exist_ok=True)

# Database settings for Render
import dj_database_url
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    } 