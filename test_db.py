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
    print(f"Database engine: {connections.databases['default'].get('ENGINE', 'Unknown')}")
    
    # Try to execute a basic query that will work on any database
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()[0]
        print(f"Basic query result: {result}")
        
        # Check if tables exist - different approach for different database types
        engine = connections.databases['default'].get('ENGINE', '')
        
        if 'sqlite' in engine:
            # For SQLite
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"Tables in SQLite database: {len(tables)}")
            for table in tables:
                print(f"  - {table[0]}")
        elif 'postgresql' in engine:
            # For PostgreSQL
            cursor.execute("SELECT COUNT(*) FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
            table_count = cursor.fetchone()[0]
            print(f"Tables in public schema: {table_count}")
            
            # List PostgreSQL tables
            cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
            tables = cursor.fetchall()
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print(f"Unknown database engine: {engine}")
    
    sys.exit(0)
except OperationalError as e:
    print(f"❌ Database connection failed: {e}")
    sys.exit(1) 