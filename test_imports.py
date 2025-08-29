#!/usr/bin/env python3
"""
Simple test to verify all imports are working
"""

def test_imports():
    """Test all imports"""
    print("Testing imports...")
    
    try:
        print("1. Testing SQLAlchemy imports...")
        from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Double, ForeignKey, DateTime
        print("   ✅ SQLAlchemy imports successful")
        
        print("2. Testing models import...")
        from models import Candidate, Education, Experience, Project, Skill, Language, Website
        print("   ✅ Models import successful")
        
        print("3. Testing CSV parser import...")
        from csv_parser import LinkedInCSVParser
        print("   ✅ CSV parser import successful")
        
        print("4. Testing config import...")
        from config import DATABASE_URL_WITH_SSL
        print("   ✅ Config import successful")
        
        print("\n🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_imports()
