#!/usr/bin/env python3
"""
Test script to verify database connection on Render
Run this locally with Render database credentials to test connection
"""

import os
import psycopg2
from urllib.parse import urlparse

def test_database_connection():
    """Test connection to Render PostgreSQL database"""
    
    # Get database URL from environment
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL environment variable not set")
        print("\nSet it like this:")
        print("export DATABASE_URL='postgresql://user:password@host:port/database'")
        return False
    
    try:
        # Parse the database URL
        parsed = urlparse(database_url)
        
        print("🔍 Testing database connection...")
        print(f"Host: {parsed.hostname}")
        print(f"Port: {parsed.port}")
        print(f"Database: {parsed.path[1:]}")  # Remove leading '/'
        print(f"User: {parsed.username}")
        
        # Connect to database
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print(f"✅ Connection successful!")
        print(f"PostgreSQL version: {version[0]}")
        
        # Test table creation (optional)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_connection (
                id SERIAL PRIMARY KEY,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("INSERT INTO test_connection (message) VALUES (%s);", ("Connection test successful!",))
        conn.commit()
        
        cursor.execute("SELECT message, created_at FROM test_connection ORDER BY created_at DESC LIMIT 1;")
        result = cursor.fetchone()
        
        print(f"✅ Database write test successful!")
        print(f"Test message: {result[0]}")
        print(f"Timestamp: {result[1]}")
        
        # Clean up
        cursor.execute("DROP TABLE test_connection;")
        conn.commit()
        
        cursor.close()
        conn.close()
        
        print("🎉 Database connection fully functional!")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_database_connection()
