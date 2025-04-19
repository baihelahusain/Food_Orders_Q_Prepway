#!/bin/bash

# Exit on error
set -o errexit

# Print each command for debugging
set -o xtrace

# Install dependencies
pip install -r requirements.txt

# Explicitly install required packages
pip install django-cors-headers whitenoise dj-database-url

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Collect static files
python manage.py collectstatic --no-input --settings=foodsite.settings_render

# Apply database migrations
python manage.py migrate --settings=foodsite.settings_render

# Create superuser if environment variables are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py createsuperuser --noinput --settings=foodsite.settings_render
fi

# Start gunicorn server with Render-specific settings
gunicorn foodsite.wsgi:application --env DJANGO_SETTINGS_MODULE=foodsite.settings_render 