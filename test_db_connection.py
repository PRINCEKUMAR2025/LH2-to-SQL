#!/usr/bin/env python3
"""
Test Database Connection Script
Tests the connection to the existing linkedin_scraper_db database
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

def test_database_connection():
    """Test the database connection"""
    print("=" * 60)
    print("Testing Database Connection to linkedin_profiles_db")
    print("=" * 60)
    
    try:
        # Load environment variables
        load_dotenv()
        
        # Get database configuration
        host = os.getenv('DB_HOST', 'localhost')
        port = os.getenv('DB_PORT', '3306')
        database = os.getenv('DB_NAME', 'linkedin_profiles_db')
        user = os.getenv('DB_USER', 'root')
        password = os.getenv('DB_PASSWORD')
        
        if not password:
            print("❌ Error: DB_PASSWORD not found in .env file")
            print("Please create a .env file with your MySQL password")
            return False
        
        # Create database URL
        database_url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}?ssl_disabled=true"
        
        print(f"Connecting to: {host}:{port}/{database}")
        print(f"User: {user}")
        
        # Test connection
        engine = create_engine(database_url)
        with engine.connect() as conn:
            # Test basic connection
            result = conn.execute(text("SELECT VERSION();"))
            version = result.fetchone()[0]
            print(f"✅ Database connection successful!")
            print(f"   MySQL version: {version}")
            
            # Test if tables exist
            result = conn.execute(text("SHOW TABLES;"))
            tables = [row[0] for row in result.fetchall()]
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table}")
            
            # Test candidate table structure
            result = conn.execute(text("DESCRIBE candidate;"))
            columns = result.fetchall()
            print(f"✅ Candidate table has {len(columns)} columns")
            
            return True
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install required packages: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\nPossible solutions:")
        print("1. Check if MySQL is running")
        print("2. Verify database credentials in .env file")
        print("3. Ensure the .env file exists and has correct values")
        return False

def main():
    """Main function"""
    print("Database Connection Test for LinkedIn CSV to SQL Converter")
    
    success = test_database_connection()
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 Database connection successful!")
        print("=" * 60)
        print("\nYou can now run the CSV converter:")
        print("1. Test with dry run: python main.py test.csv --dry-run")
        print("2. Convert your data: python main.py test.csv")
    else:
        print("\n" + "=" * 60)
        print("❌ Database connection failed!")
        print("=" * 60)
        print("\nPlease check your .env file and MySQL connection.")

if __name__ == "__main__":
    main()
