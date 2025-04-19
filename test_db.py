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
    
    # Try to execute a basic query that will work on any database
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()[0]
        print(f"Basic query result: {result}")
        
        # Check if tables exist
        cursor.execute("SELECT COUNT(*) FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
        table_count = cursor.fetchone()[0]
        print(f"Tables in public schema: {table_count}")
    
    sys.exit(0)
except OperationalError as e:
    print(f"❌ Database connection failed: {e}")
    sys.exit(1) 