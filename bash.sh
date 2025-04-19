#!/bin/bash

# Exit on error
set -o errexit

# Print each command for debugging
set -o xtrace

# First install django-cors-headers explicitly (before other deps)
pip install django-cors-headers==4.2.0

# Install requirements for Render
pip install -r requirements-render.txt

# Print pip list to debug
pip list

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Print database URL (hiding password)
if [ -n "$DATABASE_URL" ]; then
  MASKED_URL=$(echo $DATABASE_URL | sed 's/postgres:\/\/[^:]*:[^@]*@/postgres:\/\/username:***@/')
  echo "Using database: $MASKED_URL"
else
  echo "WARNING: DATABASE_URL is not set!"
fi

# Test database connection before proceeding
echo "Testing database connection..."
python test_db.py

# Collect static files
python manage.py collectstatic --no-input --settings=foodsite.settings_render

# Apply database migrations
python manage.py migrate --settings=foodsite.settings_render

# Create superuser directly with hardcoded credentials
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='baihelahusain').exists() or User.objects.create_superuser('baihelahusain', 'baihelahusain@gmail.com', 'bah@7865354')" | python manage.py shell --settings=foodsite.settings_render

# Start gunicorn server with Render-specific settings
gunicorn foodsite.wsgi:application --env DJANGO_SETTINGS_MODULE=foodsite.settings_render 