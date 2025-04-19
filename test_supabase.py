"""
Test script to verify connection to Supabase PostgreSQL database.
Run this locally with: python test_supabase.py
"""

import os
import sys
import psycopg2
from urllib.parse import quote_plus

# Supabase credentials
SUPABASE_PROJECT_ID = "jbpywpsfcnmygemtwtvz"
SUPABASE_PASSWORD = "bah@7865354"  # URL encode for safety
SUPABASE_PASSWORD_ENCODED = quote_plus(SUPABASE_PASSWORD)

# Direct connection string
CONNECTION_STRING = f"postgresql://postgres:{SUPABASE_PASSWORD_ENCODED}@db.{SUPABASE_PROJECT_ID}.supabase.co:5432/postgres"

def test_connection():
    """Test connection to Supabase PostgreSQL database"""
    print(f"Attempting to connect to Supabase database (project ID: {SUPABASE_PROJECT_ID})")
    print(f"Using connection string: postgresql://postgres:***@db.{SUPABASE_PROJECT_ID}.supabase.co:5432/postgres")
    
    try:
        # Connect to the database
        conn = psycopg2.connect(CONNECTION_STRING)
        
        # Open a cursor to perform database operations
        cur = conn.cursor()
        
        # Execute a test query
        cur.execute("SELECT version();")
        
        # Get the database version
        db_version = cur.fetchone()
        print(f"PostgreSQL database version: {db_version[0]}")
        
        # Check existing tables
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = cur.fetchall()
        
        print(f"Found {len(tables)} tables in public schema:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Close the cursor and connection
        cur.close()
        conn.close()
        
        print("✅ Successfully connected to Supabase PostgreSQL database!")
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1) 