#!/usr/bin/env python3
"""
Test script for LinkedIn Helper 2 CSV to SQL Database Converter

This script creates a sample CSV file with LinkedIn Helper 2 format data
and tests the conversion system.
"""

import pandas as pd
import os
from datetime import datetime, date
from csv_parser import LinkedInCSVParser
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sample_csv():
    """Create a sample CSV file with LinkedIn Helper 2 format data"""
    
    # Sample data that matches LinkedIn Helper 2 CSV structure
    sample_data = {
        'id': [1, 2, 3],
        'public_id': ['abc123', 'def456', 'ghi789'],
        'member_id': ['member1', 'member2', 'member3'],
        'profile_url': [
            'https://linkedin.com/in/john-doe',
            'https://linkedin.com/in/jane-smith',
            'https://linkedin.com/in/bob-johnson'
        ],
        'email': [
            'john.doe@email.com',
            'jane.smith@email.com',
            'bob.johnson@email.com'
        ],
        'full_name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'first_name': ['John', 'Jane', 'Bob'],
        'last_name': ['Doe', 'Smith', 'Johnson'],
        'original_full_name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'avatar': ['', '', ''],
        'headline': [
            'Senior Software Engineer at Tech Corp',
            'Product Manager at Startup Inc',
            'Data Scientist at Analytics Co'
        ],
        'location_name': ['San Francisco, CA', 'New York, NY', 'Austin, TX'],
        'industry': ['Technology', 'Technology', 'Technology'],
        'summary': [
            'Experienced software engineer with 5+ years in web development',
            'Product manager with expertise in SaaS products',
            'Data scientist specializing in machine learning'
        ],
        'address': ['', '', ''],
        'birthday': ['', '', ''],
        'current_company': ['Tech Corp', 'Startup Inc', 'Analytics Co'],
        'current_company_custom': ['', '', ''],
        'current_company_position': ['Senior Software Engineer', 'Product Manager', 'Data Scientist'],
        'current_company_custom_position': ['', '', ''],
        'current_company_actual_at': ['2022-01-01', '2021-06-01', '2023-03-01'],
        'current_company_industry': ['Technology', 'Technology', 'Technology'],
        
        # Organization 1 (Current job)
        'organization_1': ['Tech Corp', 'Startup Inc', 'Analytics Co'],
        'organization_id_1': ['org1', 'org2', 'org3'],
        'organization_url_1': ['', '', ''],
        'organization_title_1': ['Senior Software Engineer', 'Product Manager', 'Data Scientist'],
        'organization_start_1': ['2022-01-01', '2021-06-01', '2023-03-01'],
        'organization_end_1': ['', '', ''],  # Current position
        'organization_description_1': [
            'Developed web applications using React and Node.js',
            'Led product development for SaaS platform',
            'Built machine learning models for predictive analytics'
        ],
        'organization_location_1': ['San Francisco, CA', 'New York, NY', 'Austin, TX'],
        'organization_website_1': ['', '', ''],
        'organization_domain_1': ['', '', ''],
        'position_description_1': [
            'Full-stack development with React, Node.js, and PostgreSQL',
            'Product strategy and roadmap planning',
            'Data analysis and ML model development'
        ],
        
        # Organization 2 (Previous job)
        'organization_2': ['Previous Corp', 'Old Startup', 'Previous Analytics'],
        'organization_id_2': ['org4', 'org5', 'org6'],
        'organization_url_2': ['', '', ''],
        'organization_title_2': ['Software Engineer', 'Associate PM', 'Junior Data Scientist'],
        'organization_start_2': ['2020-01-01', '2019-06-01', '2021-03-01'],
        'organization_end_2': ['2021-12-31', '2021-05-31', '2023-02-28'],
        'organization_description_2': [
            'Developed backend services using Python and Django',
            'Assisted in product development and user research',
            'Performed data analysis and created dashboards'
        ],
        'organization_location_2': ['San Francisco, CA', 'New York, NY', 'Austin, TX'],
        'organization_website_2': ['', '', ''],
        'organization_domain_2': ['', '', ''],
        'position_description_2': [
            'Backend development with Python, Django, and MySQL',
            'User research and feature development',
            'Data visualization and statistical analysis'
        ],
        
        # Education
        'education_1': ['Stanford University', 'MIT', 'University of Texas'],
        'education_degree_1': ['Bachelor of Science', 'Master of Business Administration', 'Master of Science'],
        'education_fos_1': ['Computer Science', 'Business Administration', 'Data Science'],
        'education_start_1': ['2016-09-01', '2018-09-01', '2019-09-01'],
        'education_end_1': ['2020-06-01', '2020-06-01', '2021-06-01'],
        'education_description_1': [
            'Bachelor\'s degree in Computer Science',
            'MBA with focus on technology management',
            'Master\'s in Data Science'
        ],
        
        # Skills
        'skills': [
            'JavaScript, React, Node.js, Python, SQL, Git',
            'Product Management, Agile, User Research, Analytics, SQL',
            'Python, Machine Learning, R, SQL, Statistics, Data Visualization'
        ],
        
        # Contact information
        'phone_1': ['+1-555-0101', '+1-555-0102', '+1-555-0103'],
        'phone_type_1': ['Mobile', 'Mobile', 'Mobile'],
        'phone_2': ['+1-555-0201', '+1-555-0202', '+1-555-0203'],
        'phone_type_2': ['Work', 'Work', 'Work'],
        
        # Additional fields (empty for sample)
        'organization_3': ['', '', ''],
        'organization_4': ['', '', ''],
        'organization_5': ['', '', ''],
        'organization_6': ['', '', ''],
        'organization_7': ['', '', ''],
        'organization_8': ['', '', ''],
        'organization_9': ['', '', ''],
        'organization_10': ['', '', ''],
        'education_2': ['', '', ''],
        'education_3': ['', '', ''],
        'languages': ['English', 'English', 'English'],
        'twitters': ['', '', ''],
        'messenger_1': ['', '', ''],
        'messenger_provider_1': ['', '', ''],
        'messenger_2': ['', '', ''],
        'messenger_provider_2': ['', '', ''],
        'website_1': ['', '', ''],
        'website_2': ['', '', ''],
        'website_3': ['', '', ''],
        'followers': [500, 300, 200],
        'connections_count': [1000, 800, 600]
    }
    
    # Create DataFrame
    df = pd.DataFrame(sample_data)
    
    # Save to CSV
    filename = 'sample_linkedin_data.csv'
    df.to_csv(filename, index=False)
    
    logger.info(f"Sample CSV file created: {filename}")
    logger.info(f"Sample data contains {len(df)} candidates")
    
    return filename

def test_conversion():
    """Test the CSV to SQL conversion with sample data"""
    
    # Create sample CSV
    csv_file = create_sample_csv()
    
    try:
        # Test with dry run first
        logger.info("Testing with dry run...")
        parser = LinkedInCSVParser(csv_file)
        
        if parser.load_csv():
            logger.info("✓ CSV loading successful")
            
            # Show sample data
            logger.info("Sample data preview:")
            sample_row = parser.df.iloc[0]
            logger.info(f"  Name: {sample_row.get('full_name', 'N/A')}")
            logger.info(f"  Email: {sample_row.get('email', 'N/A')}")
            logger.info(f"  Current Company: {sample_row.get('current_company', 'N/A')}")
            logger.info(f"  Location: {sample_row.get('location_name', 'N/A')}")
            
            # Test date parsing
            logger.info("\nTesting date parsing...")
            test_dates = ['2022-01-01', 'Jan 2022', '2022', '01/2022']
            for test_date in test_dates:
                parsed = parser.parse_date(test_date)
                logger.info(f"  '{test_date}' -> {parsed}")
            
            # Test skills extraction
            logger.info("\nTesting skills extraction...")
            test_skills = "JavaScript, React, Node.js, Python, SQL, Git"
            extracted = parser.extract_skills(test_skills)
            logger.info(f"  '{test_skills}' -> {extracted}")
            
            logger.info("\n✓ All tests passed!")
            
        else:
            logger.error("✗ CSV loading failed")
            return False
            
    except Exception as e:
        logger.error(f"✗ Test failed: {e}")
        return False
    
    finally:
        # Clean up sample file
        if os.path.exists(csv_file):
            os.remove(csv_file)
            logger.info(f"Cleaned up sample file: {csv_file}")
    
    return True

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("LinkedIn Helper 2 CSV to SQL - Test Script")
    logger.info("=" * 60)
    
    success = test_conversion()
    
    if success:
        logger.info("\n🎉 All tests passed! The system is ready to use.")
        logger.info("\nNext steps:")
        logger.info("1. Configure your database connection in .env file")
        logger.info("2. Run: python main.py your_linkedin_data.csv")
        logger.info("3. Or test with: python main.py your_linkedin_data.csv --dry-run")
    else:
        logger.error("\n❌ Tests failed. Please check the configuration and try again.")
