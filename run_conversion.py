#!/usr/bin/env python3
"""
Simple script to run the LinkedIn CSV to SQL conversion
"""

import sys
import os
from csv_parser import LinkedInCSVParser
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Run the conversion"""
    print("Starting LinkedIn CSV to SQL conversion...")
    
    try:
        # Initialize parser
        parser = LinkedInCSVParser('test.csv')
        
        # Load CSV
        if not parser.load_csv():
            print("Failed to load CSV")
            return
        
        print(f"CSV loaded with {len(parser.df)} rows")
        
        # Process all rows
        success_count = 0
        total_count = len(parser.df)
        
        for index, row in parser.df.iterrows():
            print(f"Processing row {index + 1}/{total_count}")
            if parser.process_row(row):
                success_count += 1
            else:
                print(f"Failed to process row {index + 1}")
        
        print(f"Conversion complete: {success_count}/{total_count} successful")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
