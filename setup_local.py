#!/usr/bin/env python
"""
Setup script to verify the local environment for the Food Orders Q application
"""
import subprocess
import sys
import os

def check_package(package_name):
    """Check if a package is installed"""
    try:
        __import__(package_name)
        print(f"✅ {package_name} is installed")
        return True
    except ImportError:
        print(f"❌ {package_name} is NOT installed")
        return False

def install_package(package_name, version=None):
    """Install a package using pip"""
    package_spec = f"{package_name}=={version}" if version else package_name
    print(f"📦 Installing {package_spec}...")
    result = subprocess.run([sys.executable, "-m", "pip", "install", package_spec], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Successfully installed {package_spec}")
        return True
    else:
        print(f"❌ Failed to install {package_spec}:")
        print(result.stderr)
        return False

def main():
    """Main entry point"""
    print("🔍 Checking required packages...")
    
    # Check crucial packages
    corsheaders_installed = check_package("corsheaders")
    django_installed = check_package("django")
    dj_database_url_installed = check_package("dj_database_url")
    psycopg2_installed = check_package("psycopg2")
    
    # Install missing packages
    if not corsheaders_installed:
        install_package("django-cors-headers", "4.2.0")
    
    if not dj_database_url_installed:
        install_package("dj-database-url", "2.0.0")
    
    if not psycopg2_installed:
        try:
            install_package("psycopg2-binary", "2.9.6")
        except:
            print("⚠️ Could not install psycopg2-binary, trying psycopg2...")
            install_package("psycopg2", "2.9.6")
    
    # Check environment variables
    print("\n🔍 Checking environment variables...")
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        masked_url = database_url.replace(database_url.split("@")[0], "postgres://username:***")
        print(f"✅ DATABASE_URL is set: {masked_url}")
    else:
        print("❌ DATABASE_URL is not set")
        supabase_url = os.environ.get("SUPABASE_URL")
        if supabase_url:
            project_id = supabase_url.split("//")[1].split(".")[0]
            print(f"ℹ️ Detected Supabase project ID: {project_id}")
            print("ℹ️ You should set DATABASE_URL with this format:")
            print(f"postgresql://postgres:PASSWORD@db.{project_id}.supabase.co:5432/postgres?sslmode=require")
    
    render = os.environ.get("RENDER")
    if render:
        print(f"✅ RENDER is set: {render}")
    else:
        print("❌ RENDER is not set")
    
    # Print recommendations
    print("\n💡 Recommendations:")
    print("1. Make sure django-cors-headers is installed")
    print("2. Set DATABASE_URL environment variable to connect to Supabase")
    print("3. For local development, run migrations using:")
    print("   python manage.py migrate --settings=foodsite.settings")
    print("4. For testing Render-specific settings locally, run:")
    print("   python manage.py check --settings=foodsite.settings_render")
    
    print("\n✨ Setup check completed!")

if __name__ == "__main__":
    main() 