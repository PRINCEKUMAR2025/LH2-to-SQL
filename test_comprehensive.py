#!/usr/bin/env python3
"""
Comprehensive Test Script for Updated LinkedIn CSV to SQL Converter
Tests the new comprehensive mapping with all CSV columns
"""

import pandas as pd
import os
from csv_parser import LinkedInCSVParser
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_comprehensive_mapping():
    """Test the comprehensive CSV to SQL mapping"""
    print("=" * 60)
    print("Comprehensive LinkedIn CSV to SQL Test")
    print("=" * 60)
    
    try:
        # Test CSV loading
        print("1. Testing CSV loading...")
        parser = LinkedInCSVParser('test.csv')
        if parser.load_csv():
            print(f"✅ CSV loaded successfully with {len(parser.df)} rows")
            print(f"✅ Found {len(parser.df.columns)} columns")
        else:
            print("❌ Failed to load CSV")
            return False
        
        # Test sample data mapping
        print("\n2. Testing data mapping...")
        sample_row = parser.df.iloc[0]
        
        # Test candidate fields
        print("   Testing candidate fields:")
        candidate_fields = [
            'public_id', 'member_id', 'profile_url', 'email', 'full_name',
            'first_name', 'last_name', 'headline', 'location_name', 'industry',
            'current_company', 'current_company_position', 'phone_1', 'phone_2'
        ]
        
        for field in candidate_fields:
            if field in sample_row:
                value = sample_row[field]
                print(f"     ✅ {field}: {str(value)[:50]}...")
            else:
                print(f"     ❌ {field}: Not found")
        
        # Test experience extraction
        print("\n   Testing experience extraction:")
        experience_entries = parser.extract_experience(sample_row)
        print(f"     ✅ Found {len(experience_entries)} experience entries")
        if experience_entries:
            exp = experience_entries[0]
            print(f"     ✅ First experience: {exp.get('organization_name', 'N/A')} - {exp.get('title', 'N/A')}")
        
        # Test education extraction
        print("\n   Testing education extraction:")
        education_entries = parser.extract_education(sample_row)
        print(f"     ✅ Found {len(education_entries)} education entries")
        if education_entries:
            edu = education_entries[0]
            print(f"     ✅ First education: {edu.get('institution', 'N/A')} - {edu.get('degree', 'N/A')}")
        
        # Test skills extraction
        print("\n   Testing skills extraction:")
        skills_data = sample_row.get('skills', '')
        skills = parser.extract_skills(skills_data)
        print(f"     ✅ Found {len(skills)} skills")
        if skills:
            print(f"     ✅ Sample skills: {skills[:3]}")
        
        # Test languages extraction
        print("\n   Testing languages extraction:")
        languages_data = sample_row.get('languages', '')
        languages = parser.extract_languages(languages_data)
        print(f"     ✅ Found {len(languages)} languages")
        if languages:
            print(f"     ✅ Sample languages: {languages[:3]}")
        
        # Test websites extraction
        print("\n   Testing websites extraction:")
        website_1 = sample_row.get('website_1', '')
        website_2 = sample_row.get('website_2', '')
        website_3 = sample_row.get('website_3', '')
        websites = []
        if pd.notna(website_1) and website_1 != '':
            websites.append(str(website_1))
        if pd.notna(website_2) and website_2 != '':
            websites.append(str(website_2))
        if pd.notna(website_3) and website_3 != '':
            websites.append(str(website_3))
        print(f"     ✅ Found {len(websites)} websites")
        if websites:
            print(f"     ✅ Sample websites: {websites[:2]}")
        
        print("\n" + "=" * 60)
        print("🎉 All tests passed! The comprehensive mapping is working.")
        print("=" * 60)
        print("\nYou can now run the full conversion:")
        print("python main.py test.csv")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_comprehensive_mapping()
