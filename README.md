# LinkedIn Helper 2 CSV to SQL Database Converter

A comprehensive system to convert LinkedIn Helper 2 exported CSV data into a structured SQL database with separate tables for candidates, education, experience, skills, and projects.

## Features

- **Complete Data Mapping**: Maps all LinkedIn Helper 2 CSV columns to your SQL database schema
- **Multi-Table Support**: Handles candidates, education, experience, skills, and projects tables
- **Robust Date Parsing**: Supports multiple date formats commonly found in LinkedIn exports
- **Error Handling**: Comprehensive error handling with detailed logging
- **Dry Run Mode**: Test the conversion without actually inserting data
- **Progress Tracking**: Real-time progress updates during conversion
- **MySQL Support**: Optimized for MySQL database

## Database Schema

The system maps LinkedIn data to the following database tables:

### Candidate Table
- Basic candidate information (name, email, phone, location)
- Current employment details
- LinkedIn profile URL
- Calculated experience years

### Education Table
- Multiple education entries per candidate
- Institution, degree, field of study
- Start and end dates

### Experience Table
- Work history with company, position, dates
- Job descriptions and industry information

### Skills Table
- Extracted skills from LinkedIn profile
- Support for multiple skills per candidate

### Projects Table
- Project information (currently placeholder for future expansion)

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure database connection**:
   - Copy `env_example.txt` to `.env`
   - Update the database credentials in `.env`:
   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=your_database_name
   DB_USER=your_username
   DB_PASSWORD=your_password
   ```

4. **Ensure your database tables exist**:
   The system expects the following tables to be created in your database:
   - `candidate`
   - `education`
   - `experience`
   - `skills`
   - `projects`

## Usage

### Basic Usage

```bash
python main.py your_linkedin_data.csv
```

### Dry Run (Test Mode)

Test the conversion without inserting data:

```bash
python main.py your_linkedin_data.csv --dry-run
```

### Examples

```bash
# Convert a LinkedIn export file
python main.py linkedin_export.csv

# Test conversion with dry run
python main.py linkedin_export.csv --dry-run

# Convert file from different directory
python main.py /path/to/linkedin_data.csv
```

## Data Mapping

### LinkedIn CSV Columns → Database Fields

| LinkedIn Column | Database Table | Database Field | Notes |
|----------------|----------------|----------------|-------|
| `full_name` | candidate | full_name | |
| `email` | candidate | email | |
| `profile_url` | candidate | linkedin_profile | |
| `current_company` | candidate | current_company | |
| `current_company_position` | candidate | current_role | |
| `location_name` | candidate | current_location | |
| `phone_1`, `phone_2` | candidate | phone_number, whatsapp_number | Extracted and mapped |
| `education_1`, `education_degree_1`, etc. | education | institution, degree, field_of_study | Up to 3 education entries |
| `organization_1`, `organization_title_1`, etc. | experience | company, position, description | Up to 10 work experiences |
| `skills` | skills | skill_name | Parsed and split by separators |

### Calculated Fields

- **total_experience_years**: Calculated from work experience dates
- **college_name**: Extracted from first education entry
- **year_of_graduation**: Calculated from education end date

## Output

The system provides:

1. **Console Output**: Real-time progress and results
2. **Log File**: Detailed conversion log (`conversion.log`)
3. **Database Records**: Structured data in your SQL tables

### Sample Output

```
============================================================
LinkedIn Helper 2 CSV to SQL Database Converter
============================================================
Input file: linkedin_data.csv
Dry run mode: False
============================================================
Successfully loaded CSV with 150 rows
Starting to process 150 candidates...
Processing candidate 1/150
Successfully processed candidate: John Doe
...
============================================================
CONVERSION RESULTS
============================================================
Total candidates processed: 150
Successfully converted: 148
Failed conversions: 2
Success rate: 98.7%
============================================================
```

## Error Handling

The system handles various error scenarios:

- **Invalid CSV files**: Validates file format and readability
- **Database connection issues**: Graceful handling of connection problems
- **Data parsing errors**: Continues processing other records if one fails
- **Date parsing issues**: Handles various date formats with fallbacks

## Logging

All operations are logged to:
- **Console**: Real-time progress updates
- **conversion.log**: Detailed log file for debugging

## Requirements

- Python 3.7+
- MySQL database
- Required Python packages (see `requirements.txt`)

## Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Verify database credentials in `.env`
   - Ensure MySQL is running
   - Check network connectivity

2. **CSV Loading Error**:
   - Verify CSV file format
   - Check file permissions
   - Ensure file is not corrupted

3. **Data Mapping Issues**:
   - Use `--dry-run` to preview data mapping
   - Check log file for specific error details

### Getting Help

1. Run with `--dry-run` to test without database changes
2. Check `conversion.log` for detailed error information
3. Verify your CSV file matches LinkedIn Helper 2 export format

## File Structure

```
LH2_to_SQL/
├── main.py              # Main application entry point
├── csv_parser.py        # Core CSV parsing and database logic
├── models.py            # SQLAlchemy database models
├── config.py            # Database configuration
├── requirements.txt     # Python dependencies
├── env_example.txt      # Environment variables template
├── README.md           # This file
└── conversion.log      # Generated log file
```

## License

This project is provided as-is for educational and business use.
