#!/bin/bash

# Exit on error
set -o errexit

# Print each command for debugging
set -o xtrace

# Install requirements for Render specifically
pip install -r requirements-render.txt

# Explicitly install required packages
pip install django-cors-headers==4.2.0 whitenoise dj-database-url psycopg2-binary

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Print database URL (hiding password)
DATABASE_URL=$(echo $DATABASE_URL | sed 's/postgres:\/\/[^:]*:[^@]*@/postgres:\/\/username:***@/')
echo "Using database: $DATABASE_URL"

# Create a database test script
cat > test_db.py << EOF
import os
import sys
import django
from django.db import connections
from django.db.utils import OperationalError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodsite.settings_render')
django.setup()

try:
    conn = connections['default']
    conn.ensure_connection()
    print("✅ Database connection successful!")
    print(f"Connected to: {connections.databases['default'].get('HOST', 'Unknown')}")
    
    # Try to execute a query
    with conn.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"Database version: {version}")
        
        # Check if tables exist
        cursor.execute("SELECT COUNT(*) FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
        table_count = cursor.fetchone()[0]
        print(f"Tables in public schema: {table_count}")
    
    sys.exit(0)
except OperationalError as e:
    print(f"❌ Database connection failed: {e}")
    sys.exit(1)
EOF

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