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

# Create superuser directly with hardcoded credentials
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='baihelahusain').exists() or User.objects.create_superuser('baihelahusain', 'baihelahusain@gmail.com', 'bah@7865354')" | python manage.py shell --settings=foodsite.settings_render

# Start gunicorn server with Render-specific settings
gunicorn foodsite.wsgi:application --env DJANGO_SETTINGS_MODULE=foodsite.settings_render 