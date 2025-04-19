#!/bin/bash

# Exit on error
set -o errexit

# Print each command for debugging
set -o xtrace

# Check for environment variables
echo "Environment variables check:"
echo "DJANGO_SETTINGS_MODULE: ${DJANGO_SETTINGS_MODULE:-Not set}"
echo "DATABASE_URL: ${DATABASE_URL:+Set (value hidden)}"
echo "RENDER: ${RENDER:-Not set}"

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
  
  # Check if using db.jbpywpsfcnmygemtwtvz.supabase.co (direct connection)
  if [[ "$DATABASE_URL" == *"db.jbpywpsfcnmygemtwtvz.supabase.co"* ]]; then
    echo "Using direct connection URL. If this fails, will try connection pooler."
    
    # Try to test connection
    python test_db.py || {
      echo "Direct connection failed! Switching to connection pooler..."
      export DATABASE_URL="postgresql://postgres.jbpywpsfcnmygemtwtvz:bah%407865354@aws-0-us-west-1.pooler.supabase.com:6543/postgres?schema=public"
      echo "Now using pooler URL: $(echo $DATABASE_URL | sed 's/postgres:\/\/[^:]*:[^@]*@/postgres:\/\/username:***@/')"
    }
  fi
else
  echo "WARNING: DATABASE_URL is not set!"
  # Set a default DATABASE_URL using the connection pooler
  export DATABASE_URL="postgresql://postgres.jbpywpsfcnmygemtwtvz:bah%407865354@aws-0-us-west-1.pooler.supabase.com:6543/postgres?schema=public"
  echo "Setting default DATABASE_URL to Supabase connection pooler"
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