#!/usr/bin/env python3
"""
Debug script to check configuration values on Render
"""

import os
from config import get_config

def debug_configuration():
    """Debug configuration values"""
    print("🔍 Configuration Debug Information")
    print("=" * 50)
    
    # Check environment
    app_env = os.getenv('APP_ENV', 'development')
    print(f"APP_ENV: {app_env}")
    
    # Get config class
    config_class = get_config(app_env)
    print(f"Config Class: {config_class.__name__}")
    
    # Check DATABASE_URL environment variable
    database_url = os.getenv('DATABASE_URL')
    print(f"DATABASE_URL env var: {database_url[:50] + '...' if database_url and len(database_url) > 50 else database_url}")
    
    # Check individual postgres vars
    print(f"POSTGRES_HOST: {os.getenv('POSTGRES_HOST', 'NOT SET')}")
    print(f"POSTGRES_PORT: {os.getenv('POSTGRES_PORT', 'NOT SET')}")
    print(f"POSTGRES_DB: {os.getenv('POSTGRES_DB', 'NOT SET')}")
    print(f"POSTGRES_USER: {os.getenv('POSTGRES_USER', 'NOT SET')}")
    print(f"POSTGRES_PASSWORD: {'SET' if os.getenv('POSTGRES_PASSWORD') else 'NOT SET'}")
    
    # Get final database URI
    config = config_class()
    if hasattr(config, 'SQLALCHEMY_DATABASE_URI'):
        db_uri = config.SQLALCHEMY_DATABASE_URI
        if callable(db_uri):
            db_uri = db_uri
        print(f"Final SQLALCHEMY_DATABASE_URI: {db_uri[:50] + '...' if len(str(db_uri)) > 50 else db_uri}")
    
    # Test connection
    print("\n🔗 Testing Database Connection...")
    try:
        import psycopg2
        if database_url:
            conn = psycopg2.connect(database_url)
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ Connection successful: {version[:50]}...")
            cursor.close()
            conn.close()
        else:
            print("❌ No DATABASE_URL to test")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    debug_configuration()
