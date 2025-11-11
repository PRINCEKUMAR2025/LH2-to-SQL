#!/usr/bin/env python3
"""
Database Setup Script for LinkedIn Helper 2 CSV to SQL Converter

This script helps you set up your database connection and create the necessary tables.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError
import getpass

def create_env_file():
    """Create .env file with database configuration"""
    print("=" * 60)
    print("LinkedIn Helper 2 CSV to SQL - Database Setup")
    print("=" * 60)
    
    print("\nPlease provide your MySQL database configuration:")
    
    # Get database configuration from user
    host = input("Database Host (default: localhost): ").strip() or "localhost"
    port = input("Database Port (default: 3306): ").strip() or "3306"
    database = input("Database Name (default: linkedin_candidates): ").strip() or "linkedin_candidates"
    user = input("Database Username (default: root): ").strip() or "root"
    password = getpass.getpass("Database Password: ").strip()
    
    if not password:
        print("❌ Password is required!")
        return False
    
    # Create .env content
    env_content = f"""# Database Configuration
DB_HOST={host}
DB_PORT={port}
DB_NAME={database}
DB_USER={user}
DB_PASSWORD={password}
"""
    
    # Write to .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def test_database_connection():
    """Test the database connection"""
    print("\n" + "=" * 40)
    print("Testing Database Connection")
    print("=" * 40)
    
    try:
        # Reload environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        from config import DATABASE_URL_WITH_SSL
        
        # Test connection
        engine = create_engine(DATABASE_URL_WITH_SSL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Database connection successful!")
            print(f"   MySQL version: {version}")
            return True
            
    except ImportError:
        print("❌ Error: Could not import required modules.")
        print("   Please run: pip install -r requirements.txt")
        return False
    except OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        print("\nPossible solutions:")
        print("1. Check if MySQL is running")
        print("2. Verify database credentials in .env file")
        print("3. Ensure database exists")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def create_tables():
    """Create the necessary database tables"""
    print("\n" + "=" * 40)
    print("Creating Database Tables")
    print("=" * 40)
    
    try:
        from config import DATABASE_URL_WITH_SSL
        from models import Base, engine
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Verify tables exist
        with engine.connect() as conn:
            tables = ['candidate', 'education', 'experience', 'skills', 'projects', 'languages', 'websites', 'yearofexp']
            for table in tables:
                result = conn.execute(text(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table}');"))
                exists = result.fetchone()[0]
                if exists:
                    print(f"   ✅ Table '{table}' exists")
                else:
                    print(f"   ❌ Table '{table}' missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def main():
    """Main setup function"""
    print("LinkedIn Helper 2 CSV to SQL Database Setup")
    print("This script will help you configure your database connection.")
    
    # Step 1: Create .env file
    if not create_env_file():
        return False
    
    # Step 2: Test database connection
    if not test_database_connection():
        return False
    
    # Step 3: Create tables
    if not create_tables():
        return False
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("=" * 60)
    print("\nYou can now run the CSV converter:")
    print("1. Test with dry run: python main.py test.csv --dry-run")
    print("2. Convert your data: python main.py test.csv")
    print("\nIf you encounter any issues, check the .env file and ensure MySQL is running.")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
