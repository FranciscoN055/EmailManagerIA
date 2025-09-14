#!/usr/bin/env python3
"""
SQLite database initialization script for Email Manager IA Production
This script uses SQLite for production as a fallback
"""

import os
import sys
from flask import Flask

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def init_database_sqlite_prod():
    """Initialize SQLite database for production."""
    try:
        print("🚀 Starting SQLite database initialization for production...")
        
        # Create Flask app
        from app import create_app, db
        app = create_app()
        print(f"✅ Flask app created with environment: {app.config.get('FLASK_ENV', 'unknown')}")
        
        with app.app_context():
            print("🚀 Initializing SQLite database...")
            print(f"📊 Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')[:50]}...")
            
            # Test database connection
            try:
                db.session.execute('SELECT 1')
                print("✅ Database connection successful!")
            except Exception as e:
                print(f"❌ Database connection failed: {e}")
                return False
            
            # Create all tables
            print("🔄 Creating database tables...")
            db.create_all()
            print("✅ Tables created successfully!")
            
            # Verify tables were created
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📊 Tables created: {tables}")
            
            print("✅ SQLite database initialized successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Error initializing SQLite database: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = init_database_sqlite_prod()
    if not success:
        print("❌ SQLite initialization failed")
        sys.exit(1)
    else:
        print("✅ SQLite initialization completed successfully!")
        sys.exit(0)
