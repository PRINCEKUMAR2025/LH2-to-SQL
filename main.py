#!/usr/bin/env python3
"""
LinkedIn Helper 2 CSV to SQL Database Converter

This script converts LinkedIn Helper 2 exported CSV data into a structured SQL database
with separate tables for candidates, education, experience, skills, and projects.

Usage:
    python main.py <csv_file_path>
    
Example:
    python main.py linkedin_data.csv
"""

import sys
import os
import argparse
from csv_parser import LinkedInCSVParser
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('conversion.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def validate_csv_file(file_path: str) -> bool:
    """Validate that the CSV file exists and is readable"""
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return False
    
    if not file_path.lower().endswith('.csv'):
        logger.error(f"File must be a CSV file: {file_path}")
        return False
    
    if not os.access(file_path, os.R_OK):
        logger.error(f"File is not readable: {file_path}")
        return False
    
    return True

def main():
    """Main function to handle CSV to SQL conversion"""
    parser = argparse.ArgumentParser(
        description='Convert LinkedIn Helper 2 CSV data to SQL database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py linkedin_data.csv
  python main.py /path/to/linkedin_export.csv
        """
    )
    
    parser.add_argument(
        'csv_file',
        help='Path to the LinkedIn Helper 2 CSV file'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform a dry run without actually inserting data into the database'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not validate_csv_file(args.csv_file):
        sys.exit(1)
    
    logger.info("=" * 60)
    logger.info("LinkedIn Helper 2 CSV to SQL Database Converter")
    logger.info("=" * 60)
    logger.info(f"Input file: {args.csv_file}")
    logger.info(f"Dry run mode: {args.dry_run}")
    logger.info("=" * 60)
    
    try:
        # Initialize parser
        parser = LinkedInCSVParser(args.csv_file)
        
        if args.dry_run:
            # Load CSV and show preview
            if parser.load_csv():
                logger.info(f"CSV loaded successfully with {len(parser.df)} rows")
                logger.info("First few columns:")
                for col in parser.df.columns[:10]:
                    logger.info(f"  - {col}")
                logger.info("...")
                
                # Show sample data
                logger.info("\nSample data (first row):")
                sample_row = parser.df.iloc[0]
                for col in ['full_name', 'email', 'current_company', 'location_name']:
                    if col in sample_row:
                        logger.info(f"  {col}: {sample_row[col]}")
                
                logger.info("\nDry run completed. No data was inserted into the database.")
            else:
                logger.error("Failed to load CSV file")
                sys.exit(1)
        else:
            # Process the CSV file
            logger.info("Starting CSV to SQL conversion...")
            results = parser.process_all()
            
            # Display results
            logger.info("=" * 60)
            logger.info("CONVERSION RESULTS")
            logger.info("=" * 60)
            logger.info(f"Total candidates processed: {results['total']}")
            logger.info(f"Successfully converted: {results['success']}")
            logger.info(f"Failed conversions: {results['failed']}")
            logger.info(f"Success rate: {(results['success']/results['total']*100):.1f}%" if results['total'] > 0 else "N/A")
            logger.info("=" * 60)
            
            if results['failed'] > 0:
                logger.warning(f"{results['failed']} candidates failed to convert. Check the log file for details.")
                sys.exit(1)
            else:
                logger.info("All candidates converted successfully!")
    
    except KeyboardInterrupt:
        logger.info("\nConversion interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
