"""
Database Adapter for SQLite and PostgreSQL compatibility
محول قاعدة البيانات لدعم SQLite و PostgreSQL

This module provides compatibility between SQLite (development) and PostgreSQL (production).
يوفر هذا الملف التوافق بين SQLite (التطوير) و PostgreSQL (الإنتاج).
"""

import os
import sys
from urllib.parse import urlparse

def get_database_type():
    """
    Determine which database to use based on environment
    تحديد نوع قاعدة البيانات بناءً على البيئة
    """
    database_url = os.environ.get('DATABASE_URL', '')
    
    if database_url and database_url.startswith('postgres'):
        return 'postgresql'
    return 'sqlite'

def get_connection_params():
    """
    Get database connection parameters based on environment
    الحصول على معاملات الاتصال بقاعدة البيانات
    """
    db_type = get_database_type()
    
    if db_type == 'postgresql':
        database_url = os.environ.get('DATABASE_URL', '')
        
        # Parse the database URL
        if database_url:
            # Render uses postgres:// but psycopg2 needs postgresql://
            if database_url.startswith('postgres://'):
                database_url = database_url.replace('postgres://', 'postgresql://', 1)
            
            return {
                'type': 'postgresql',
                'url': database_url
            }
    
    # Default to SQLite
    return {
        'type': 'sqlite',
        'path': os.path.join(os.path.dirname(__file__), 'housing.db')
    }

def get_db_connection():
    """
    Create and return a database connection based on environment
    إنشاء وإرجاع اتصال قاعدة البيانات بناءً على البيئة
    """
    params = get_connection_params()
    
    if params['type'] == 'postgresql':
        try:
            import psycopg2
            import psycopg2.extras
            
            conn = psycopg2.connect(params['url'])
            # Enable dict-like row access
            conn.cursor_factory = psycopg2.extras.RealDictCursor
            return conn
        except ImportError:
            print("⚠️  Warning: psycopg2 not installed. Falling back to SQLite.")
            print("Install with: pip install psycopg2-binary")
        except Exception as e:
            print(f"⚠️  Warning: Could not connect to PostgreSQL: {e}")
            print("Falling back to SQLite.")
    
    # Fall back to SQLite
    import sqlite3
    conn = sqlite3.connect(params['path'])
    conn.row_factory = sqlite3.Row
    return conn

def get_placeholder():
    """
    Get the appropriate placeholder for SQL queries
    الحصول على العنصر النائب المناسب لاستعلامات SQL
    
    SQLite uses ? while PostgreSQL uses %s
    """
    params = get_connection_params()
    return '%s' if params['type'] == 'postgresql' else '?'

def adapt_sql(sql_query):
    """
    Adapt SQL query for the current database type
    تكييف استعلام SQL لنوع قاعدة البيانات الحالي
    
    Converts SQLite-specific syntax to PostgreSQL-compatible syntax
    """
    params = get_connection_params()
    
    if params['type'] == 'postgresql':
        # Convert AUTOINCREMENT to SERIAL
        sql_query = sql_query.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
        sql_query = sql_query.replace('AUTOINCREMENT', '')
        
        # Convert TEXT to VARCHAR where appropriate
        # Keep TEXT as is, as PostgreSQL supports it
        
        # Convert CURRENT_TIMESTAMP (SQLite) to NOW() or CURRENT_TIMESTAMP (PostgreSQL)
        # Both work in PostgreSQL, so no change needed
        
        # Replace ? placeholders with %s
        count = sql_query.count('?')
        for i in range(count):
            sql_query = sql_query.replace('?', '%s', 1)
    
    return sql_query

def print_database_info():
    """
    Print current database configuration
    طباعة معلومات قاعدة البيانات الحالية
    """
    params = get_connection_params()
    db_type = params['type']
    
    print("\n" + "="*60)
    print("📊 Database Configuration / تكوين قاعدة البيانات")
    print("="*60)
    
    if db_type == 'postgresql':
        print("✅ Database Type: PostgreSQL")
        print("🌐 Environment: Production (Render.com)")
        print(f"🔗 Connection: {params['url'][:30]}...")
    else:
        print("✅ Database Type: SQLite")
        print("💻 Environment: Development (Local)")
        print(f"📁 Database Path: {params['path']}")
    
    print("="*60 + "\n")

if __name__ == '__main__':
    # Test the database adapter
    print_database_info()
    
    try:
        conn = get_db_connection()
        print("✅ Database connection successful!")
        conn.close()
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
