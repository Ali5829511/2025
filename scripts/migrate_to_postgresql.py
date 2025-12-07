#!/usr/bin/env python3
"""
SQLite to PostgreSQL Migration Script
سكريبت ترحيل من SQLite إلى PostgreSQL

This script migrates data from SQLite database to PostgreSQL.
يقوم هذا السكريبت بترحيل البيانات من قاعدة بيانات SQLite إلى PostgreSQL.
"""

import sys
import os
import sqlite3
import psycopg2
from psycopg2 import sql, extras
from datetime import datetime
from urllib.parse import urlparse
import logging
import subprocess
import shutil
import re

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
SQLITE_DB = os.environ.get('SQLITE_DB', 'housing.db')
DATABASE_URL = os.environ.get('DATABASE_URL', '')


def parse_postgres_url(url):
    """Parse PostgreSQL connection URL"""
    parsed = urlparse(url)
    return {
        'host': parsed.hostname,
        'port': parsed.port or 5432,
        'database': parsed.path[1:],
        'user': parsed.username,
        'password': parsed.password
    }


def get_sqlite_connection():
    """Get SQLite database connection"""
    if not os.path.exists(SQLITE_DB):
        logger.error(f"❌ SQLite database not found: {SQLITE_DB}")
        sys.exit(1)
    
    conn = sqlite3.connect(SQLITE_DB)
    conn.row_factory = sqlite3.Row
    return conn


def get_postgres_connection():
    """Get PostgreSQL database connection"""
    if not DATABASE_URL:
        logger.error("❌ DATABASE_URL environment variable not set")
        logger.info("Example: export DATABASE_URL='postgresql://user:password@host:port/database'")
        sys.exit(1)
    
    try:
        conn_params = parse_postgres_url(DATABASE_URL)
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = False
        return conn
    except Exception as e:
        logger.error(f"❌ Failed to connect to PostgreSQL: {e}")
        sys.exit(1)


def create_postgres_schema(pg_conn):
    """Create PostgreSQL schema"""
    logger.info("📋 Creating PostgreSQL schema...")
    
    cursor = pg_conn.cursor()
    
    # Read the schema from init_db.py or create it here
    schema_sql = """
    -- Users table
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        name VARCHAR(200) NOT NULL,
        email VARCHAR(200) UNIQUE,
        phone VARCHAR(20),
        role VARCHAR(50) NOT NULL DEFAULT 'viewer',
        is_active BOOLEAN DEFAULT TRUE,
        must_change_password BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Sessions table
    CREATE TABLE IF NOT EXISTS sessions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        session_token VARCHAR(255) UNIQUE NOT NULL,
        ip_address VARCHAR(50),
        user_agent TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP NOT NULL
    );
    
    -- Buildings table
    CREATE TABLE IF NOT EXISTS buildings (
        id SERIAL PRIMARY KEY,
        building_number VARCHAR(50) UNIQUE NOT NULL,
        name VARCHAR(200) NOT NULL,
        location VARCHAR(200),
        total_floors INTEGER,
        total_units INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Residents table
    CREATE TABLE IF NOT EXISTS residents (
        id SERIAL PRIMARY KEY,
        national_id VARCHAR(20) UNIQUE NOT NULL,
        name VARCHAR(200) NOT NULL,
        email VARCHAR(200),
        phone VARCHAR(20),
        department VARCHAR(200),
        job_title VARCHAR(200),
        building_id INTEGER REFERENCES buildings(id),
        unit_number VARCHAR(50),
        move_in_date DATE,
        move_out_date DATE,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Vehicles table
    CREATE TABLE IF NOT EXISTS vehicles (
        id SERIAL PRIMARY KEY,
        owner_id INTEGER REFERENCES residents(id),
        plate_number VARCHAR(50) UNIQUE NOT NULL,
        vehicle_type VARCHAR(100),
        make VARCHAR(100),
        model VARCHAR(100),
        year INTEGER,
        color VARCHAR(50),
        sticker_number VARCHAR(50),
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Traffic violations table
    CREATE TABLE IF NOT EXISTS traffic_violations (
        id SERIAL PRIMARY KEY,
        vehicle_id INTEGER REFERENCES vehicles(id),
        violation_type VARCHAR(200) NOT NULL,
        violation_date TIMESTAMP NOT NULL,
        location VARCHAR(200),
        fine_amount DECIMAL(10, 2),
        status VARCHAR(50) DEFAULT 'open',
        description TEXT,
        officer_name VARCHAR(200),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Security incidents table
    CREATE TABLE IF NOT EXISTS security_incidents (
        id SERIAL PRIMARY KEY,
        incident_type VARCHAR(200) NOT NULL,
        incident_date TIMESTAMP NOT NULL,
        location VARCHAR(200),
        description TEXT,
        reporter_name VARCHAR(200),
        status VARCHAR(50) DEFAULT 'open',
        severity VARCHAR(50),
        resolution TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Complaints table
    CREATE TABLE IF NOT EXISTS complaints (
        id SERIAL PRIMARY KEY,
        resident_id INTEGER REFERENCES residents(id),
        complaint_type VARCHAR(200) NOT NULL,
        description TEXT NOT NULL,
        status VARCHAR(50) DEFAULT 'open',
        priority VARCHAR(50),
        submitted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        resolved_date TIMESTAMP,
        resolution TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Audit log table
    CREATE TABLE IF NOT EXISTS audit_log (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        action VARCHAR(200) NOT NULL,
        details TEXT,
        ip_address VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Apartments table
    CREATE TABLE IF NOT EXISTS apartments (
        id SERIAL PRIMARY KEY,
        building_id INTEGER REFERENCES buildings(id),
        unit_number VARCHAR(50) NOT NULL,
        floor_number INTEGER,
        unit_type VARCHAR(100),
        bedrooms INTEGER,
        bathrooms INTEGER,
        area_sqm DECIMAL(10, 2),
        is_occupied BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Parking spots table
    CREATE TABLE IF NOT EXISTS parking_spots (
        id SERIAL PRIMARY KEY,
        building_id INTEGER REFERENCES buildings(id),
        spot_number VARCHAR(50) NOT NULL,
        level INTEGER,
        is_occupied BOOLEAN DEFAULT FALSE,
        vehicle_id INTEGER REFERENCES vehicles(id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Stickers table
    CREATE TABLE IF NOT EXISTS stickers (
        id SERIAL PRIMARY KEY,
        sticker_number VARCHAR(50) UNIQUE NOT NULL,
        vehicle_id INTEGER REFERENCES vehicles(id),
        issue_date DATE NOT NULL,
        expiry_date DATE NOT NULL,
        status VARCHAR(50) DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Visitors table
    CREATE TABLE IF NOT EXISTS visitors (
        id SERIAL PRIMARY KEY,
        name VARCHAR(200) NOT NULL,
        national_id VARCHAR(20),
        phone VARCHAR(20),
        vehicle_plate VARCHAR(50),
        visiting_resident_id INTEGER REFERENCES residents(id),
        purpose VARCHAR(200),
        entry_time TIMESTAMP,
        exit_time TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Plate recognition log table
    CREATE TABLE IF NOT EXISTS plate_recognition_log (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        plate_number VARCHAR(50) NOT NULL,
        confidence DECIMAL(5, 4),
        vehicle_id INTEGER REFERENCES vehicles(id),
        recognized_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- API tokens table
    CREATE TABLE IF NOT EXISTS api_tokens (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        token_name VARCHAR(200) NOT NULL,
        token_hash VARCHAR(255) UNIQUE NOT NULL,
        description TEXT,
        permissions VARCHAR(50) DEFAULT 'read',
        expires_at TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE,
        created_by INTEGER REFERENCES users(id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_used_at TIMESTAMP
    );
    
    -- API token usage log table
    CREATE TABLE IF NOT EXISTS api_token_usage_log (
        id SERIAL PRIMARY KEY,
        token_id INTEGER REFERENCES api_tokens(id) ON DELETE CASCADE,
        endpoint VARCHAR(200),
        method VARCHAR(10),
        ip_address VARCHAR(50),
        user_agent TEXT,
        status_code INTEGER,
        response_time_ms INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Car images table
    CREATE TABLE IF NOT EXISTS car_images (
        id SERIAL PRIMARY KEY,
        original_filename VARCHAR(255) NOT NULL,
        image_path VARCHAR(500) NOT NULL,
        thumbnail_path VARCHAR(500),
        uploaded_by INTEGER REFERENCES users(id),
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Car analysis table
    CREATE TABLE IF NOT EXISTS car_analysis (
        id SERIAL PRIMARY KEY,
        car_image_id INTEGER REFERENCES car_images(id) ON DELETE CASCADE,
        vehicle_id INTEGER REFERENCES vehicles(id),
        plate_number VARCHAR(50),
        plate_confidence DECIMAL(5, 4),
        vehicle_type VARCHAR(100),
        vehicle_color VARCHAR(50),
        make VARCHAR(100),
        model VARCHAR(100),
        analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Create indexes
    CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
    CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(session_token);
    CREATE INDEX IF NOT EXISTS idx_sessions_expires ON sessions(expires_at);
    CREATE INDEX IF NOT EXISTS idx_residents_building ON residents(building_id);
    CREATE INDEX IF NOT EXISTS idx_residents_national_id ON residents(national_id);
    CREATE INDEX IF NOT EXISTS idx_vehicles_owner ON vehicles(owner_id);
    CREATE INDEX IF NOT EXISTS idx_vehicles_plate ON vehicles(plate_number);
    CREATE INDEX IF NOT EXISTS idx_violations_vehicle ON traffic_violations(vehicle_id);
    CREATE INDEX IF NOT EXISTS idx_violations_date ON traffic_violations(violation_date);
    CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_log(user_id);
    CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_log(created_at);
    CREATE INDEX IF NOT EXISTS idx_plate_recognition_vehicle ON plate_recognition_log(vehicle_id);
    CREATE INDEX IF NOT EXISTS idx_api_tokens_user ON api_tokens(user_id);
    CREATE INDEX IF NOT EXISTS idx_api_token_usage_token ON api_token_usage_log(token_id);
    """
    
    try:
        cursor.execute(schema_sql)
        pg_conn.commit()
        logger.info("✅ PostgreSQL schema created successfully")
    except Exception as e:
        logger.error(f"❌ Failed to create schema: {e}")
        pg_conn.rollback()
        raise


def validate_table_name(table_name):
    """
    Validate table name to prevent SQL injection.
    
    Security Note:
    All table names are validated before use to prevent SQL injection.
    For SQLite queries, validated table names are used in f-strings (safe after validation).
    For PostgreSQL queries, we use psycopg2.sql.Identifier for additional safety.
    """
    # Allow only alphanumeric characters and underscores
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table_name):
        raise ValueError(f"Invalid table name: {table_name}")
    return table_name


def migrate_table(sqlite_conn, pg_conn, table_name, batch_size=1000):
    """Migrate data from SQLite table to PostgreSQL"""
    logger.info(f"📊 Migrating table: {table_name}")
    
    # Validate table name
    table_name = validate_table_name(table_name)
    
    sqlite_cursor = sqlite_conn.cursor()
    pg_cursor = pg_conn.cursor()
    
    try:
        # Get total count
        # For SQLite: table name is already validated, safe to use in f-string
        sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        total = sqlite_cursor.fetchone()[0]
        total = sqlite_cursor.fetchone()[0]
        
        if total == 0:
            logger.info(f"  ⚠️  Table {table_name} is empty, skipping")
            return
        
        # Get column names (SQLite query with validated table name)
        sqlite_cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
        columns = [description[0] for description in sqlite_cursor.description]
        
        # Adjust column names for PostgreSQL (id is auto-increment)
        insert_columns = [col for col in columns if col != 'id']
        
        # Fetch and insert data in batches (SQLite query with validated table name)
        sqlite_cursor.execute(f"SELECT * FROM {table_name}")
        
        migrated = 0
        while True:
            rows = sqlite_cursor.fetchmany(batch_size)
            if not rows:
                break
            
            # Prepare data for insertion
            values = []
            for row in rows:
                row_dict = dict(row)
                # Remove id column
                row_dict.pop('id', None)
                values.append(tuple(row_dict.values()))
            
            # Build insert query using psycopg2.sql for safe table/column names
            insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                sql.SQL(',').join(map(sql.Identifier, insert_columns)),
                sql.SQL(',').join(sql.Placeholder() * len(insert_columns))
            )
            
            # Execute batch insert
            extras.execute_batch(pg_cursor, insert_query, values)
            pg_conn.commit()
            
            migrated += len(rows)
            logger.info(f"  ✓ Migrated {migrated}/{total} rows from {table_name}")
        
        # Reset sequence for id column using sql.Identifier
        reset_query = sql.SQL("""
            SELECT setval(pg_get_serial_sequence({}, 'id'), 
                         COALESCE((SELECT MAX(id) FROM {}), 1), 
                         true)
        """).format(sql.Literal(table_name), sql.Identifier(table_name))
        pg_cursor.execute(reset_query)
        pg_conn.commit()
        
        logger.info(f"✅ Table {table_name} migrated successfully ({migrated} rows)")
        
    except Exception as e:
        logger.error(f"❌ Failed to migrate table {table_name}: {e}")
        pg_conn.rollback()
        raise


def verify_migration(sqlite_conn, pg_conn):
    """Verify data migration"""
    logger.info("🔍 Verifying migration...")
    
    sqlite_cursor = sqlite_conn.cursor()
    pg_cursor = pg_conn.cursor()
    
    # Get list of tables
    sqlite_cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
    """)
    tables = [row[0] for row in sqlite_cursor.fetchall()]
    
    all_match = True
    for table in tables:
        try:
            # Validate table name
            table = validate_table_name(table)
            
            # Count rows in SQLite (validated table name, safe to use in f-string)
            sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table}")
            sqlite_count = sqlite_cursor.fetchone()[0]
            
            # Count rows in PostgreSQL using safe query
            count_query = sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(table))
            pg_cursor.execute(count_query)
            pg_count = pg_cursor.fetchone()[0]
            
            if sqlite_count == pg_count:
                logger.info(f"  ✅ {table}: {sqlite_count} rows match")
            else:
                logger.warning(f"  ⚠️  {table}: SQLite={sqlite_count}, PostgreSQL={pg_count}")
                all_match = False
                
        except Exception as e:
            logger.warning(f"  ⚠️  Could not verify table {table}: {e}")
    
    if all_match:
        logger.info("✅ All tables verified successfully")
    else:
        logger.warning("⚠️  Some tables have mismatched row counts")
    
    return all_match


def main():
    """Main migration function"""
    logger.info("=" * 60)
    logger.info("SQLite to PostgreSQL Migration")
    logger.info("ترحيل من SQLite إلى PostgreSQL")
    logger.info("=" * 60)
    logger.info("")
    
    # Check if backup exists
    backup_file = f"{SQLITE_DB}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    logger.info(f"📦 Creating backup: {backup_file}")
    try:
        shutil.copy2(SQLITE_DB, backup_file)
    except Exception as e:
        logger.error(f"Failed to create backup: {e}")
        sys.exit(1)
    
    # Get connections
    logger.info("🔌 Connecting to databases...")
    sqlite_conn = get_sqlite_connection()
    pg_conn = get_postgres_connection()
    logger.info("✅ Connected to both databases")
    
    try:
        # Create PostgreSQL schema
        create_postgres_schema(pg_conn)
        
        # Get list of tables to migrate
        sqlite_cursor = sqlite_conn.cursor()
        sqlite_cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tables = [row[0] for row in sqlite_cursor.fetchall()]
        
        logger.info(f"📋 Found {len(tables)} tables to migrate")
        logger.info("")
        
        # Migrate each table
        for table in tables:
            migrate_table(sqlite_conn, pg_conn, table)
            logger.info("")
        
        # Verify migration
        logger.info("")
        verify_migration(sqlite_conn, pg_conn)
        
        logger.info("")
        logger.info("=" * 60)
        logger.info("✅ Migration completed successfully!")
        logger.info("✅ اكتمل الترحيل بنجاح!")
        logger.info("=" * 60)
        logger.info("")
        logger.info("Next steps:")
        logger.info("1. Verify application works with PostgreSQL")
        logger.info("2. Update DATABASE_URL in production environment")
        logger.info("3. Keep SQLite backup for rollback if needed")
        logger.info(f"4. Backup file: {backup_file}")
        
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        logger.error("💡 The SQLite database was not modified")
        logger.error(f"💡 Backup available at: {backup_file}")
        sys.exit(1)
    
    finally:
        sqlite_conn.close()
        pg_conn.close()


if __name__ == '__main__':
    main()
