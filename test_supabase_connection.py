import psycopg2
import sys

def test_connection():
    connection_string = 'postgres://postgres.jbpywpsfcnmygemtwtvz:bah%407865354@aws-0-ap-south-1.pooler.supabase.com:6543/postgres'
    
    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute('SELECT version();')
        db_version = cursor.fetchone()
        
        print("Connection successful!")
        print(f"PostgreSQL version: {db_version[0]}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1) 