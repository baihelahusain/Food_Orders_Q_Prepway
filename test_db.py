import os
import sys
import socket
import django
from django.db import connections
from django.db.utils import OperationalError

# Print network connectivity information
print("\n--- Network Diagnostics ---")
try:
    # Try to get local IP
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"Hostname: {hostname}")
    print(f"Local IP: {local_ip}")
    
    # Check IPv6 support
    has_ipv6 = False
    try:
        socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        has_ipv6 = True
    except (socket.error, ImportError):
        pass
    
    print(f"IPv6 Support: {'Yes' if has_ipv6 else 'No'}")
    
    # Get database connection info
    db_url = os.environ.get('DATABASE_URL', 'Not set')
    masked_url = 'Not set'
    host = 'unknown'
    
    if db_url != 'Not set':
        # Mask password in URL
        parts = db_url.split('@')
        if len(parts) > 1:
            masked_url = parts[0].split(':')[0] + ':***@' + parts[1]
            
        # Extract host
        if '@' in db_url:
            host_part = db_url.split('@')[1].split('/')[0]
            host = host_part.split(':')[0]
    
    print(f"Database URL: {masked_url}")
    print(f"Database Host: {host}")
    
    # Try to resolve database host
    if host != 'unknown':
        try:
            print(f"Resolving {host}...")
            ip_info = socket.getaddrinfo(host, None)
            for ip in ip_info:
                ip_version = "IPv4" if ip[0] == socket.AF_INET else "IPv6"
                print(f"  → {ip_version}: {ip[4][0]}")
        except socket.gaierror as e:
            print(f"  → DNS resolution failed: {e}")
    
except Exception as e:
    print(f"Error in network diagnostics: {e}")

print("--- End Network Diagnostics ---\n")

# Set up Django
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
            try:
                # First try the PostgreSQL-specific query
                cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
                tables = cursor.fetchall()
                print(f"Tables in PostgreSQL database: {len(tables)}")
                for table in tables:
                    print(f"  - {table[0]}")
            except Exception as e:
                print(f"Error listing tables with pg_tables: {e}")
                # Fallback to a more compatible query
                try:
                    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
                    tables = cursor.fetchall()
                    print(f"Tables from information_schema: {len(tables)}")
                    for table in tables:
                        print(f"  - {table[0]}")
                except Exception as e2:
                    print(f"Error listing tables with information_schema: {e2}")
        else:
            print(f"Unknown database engine: {engine}")
    
    sys.exit(0)
except OperationalError as e:
    print(f"❌ Database connection failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1) 