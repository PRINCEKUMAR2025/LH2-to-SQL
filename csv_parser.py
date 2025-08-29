import pandas as pd
import numpy as np
from datetime import datetime, date
import re
from typing import List, Dict, Any, Optional
from models import Candidate, Education, Experience, Project, Skill, Language, Website, SessionLocal
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LinkedInCSVParser:
    def __init__(self, csv_file_path: str):
        self.csv_file_path = csv_file_path
        self.df = None
        try:
            self.db = SessionLocal()
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            logger.error("Please run 'python setup_database.py' to configure your database connection.")
            raise
        
    def load_csv(self):
        """Load the CSV file into a pandas DataFrame"""
        try:
            self.df = pd.read_csv(self.csv_file_path)
            logger.info(f"Successfully loaded CSV with {len(self.df)} rows")
            return True
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            return False
    
    def parse_date(self, date_str: str) -> Optional[date]:
        """Parse date string to date object"""
        if pd.isna(date_str) or date_str == '':
            return None
        
        try:
            # Handle various date formats
            if isinstance(date_str, str):
                # Remove extra spaces and common prefixes
                date_str = date_str.strip()
                
                # Try different date formats
                date_formats = [
                    '%Y-%m-%d',
                    '%m/%d/%Y',
                    '%d/%m/%Y',
                    '%Y/%m/%d',
                    '%m-%d-%Y',
                    '%d-%m-%Y',
                    '%b %Y',
                    '%B %Y',
                    '%Y',
                    '%m/%Y',
                    '%Y/%m'
                ]
                
                for fmt in date_formats:
                    try:
                        return datetime.strptime(date_str, fmt).date()
                    except ValueError:
                        continue
                
                # If no format matches, try to extract year only
                year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
                if year_match:
                    return datetime.strptime(year_match.group(), '%Y').date()
            
            return None
        except Exception as e:
            logger.warning(f"Could not parse date: {date_str}, error: {e}")
            return None
    
    def extract_languages(self, languages_data: str) -> List[str]:
        """Extract languages from LinkedIn data"""
        if pd.isna(languages_data) or languages_data == '':
            return []
        
        # Split languages by common separators
        languages = re.split(r'[,;|•]', str(languages_data))
        
        # Clean and filter languages
        cleaned_languages = []
        for language in languages:
            language = language.strip()
            if language and len(language) > 1:  # Filter out empty or single character languages
                cleaned_languages.append(language)
        
        return cleaned_languages[:10]  # Limit to 10 languages
    
    def extract_websites(self, website_data: str) -> List[str]:
        """Extract websites from LinkedIn data"""
        if pd.isna(website_data) or website_data == '':
            return []
        
        # Split websites by common separators
        websites = re.split(r'[,;|]', str(website_data))
        
        # Clean and filter websites
        cleaned_websites = []
        for website in websites:
            website = website.strip()
            if website and ('http' in website or '.' in website):  # Basic URL validation
                cleaned_websites.append(website)
        
        return cleaned_websites[:5]  # Limit to 5 websites
    
    def extract_skills(self, skills_data: str) -> List[str]:
        """Extract skills from LinkedIn data"""
        if pd.isna(skills_data) or skills_data == '':
            return []
        
        # Split skills by common separators
        skills = re.split(r'[,;|•]', str(skills_data))
        
        # Clean and filter skills
        cleaned_skills = []
        for skill in skills:
            skill = skill.strip()
            if skill and len(skill) > 1:  # Filter out empty or single character skills
                cleaned_skills.append(skill)
        
        return cleaned_skills[:20]  # Limit to 20 skills
    
    def extract_education(self, row: pd.Series) -> List[Dict[str, Any]]:
        """Extract education information from LinkedIn data"""
        education_entries = []
        
        # Check for education data (up to 3 education entries)
        for i in range(1, 4):
            institution = row.get(f'education_{i}', '')
            degree = row.get(f'education_degree_{i}', '')
            field_of_study = row.get(f'education_fos_{i}', '')
            start_date = row.get(f'education_start_{i}', '')
            end_date = row.get(f'education_end_{i}', '')
            description = row.get(f'education_description_{i}', '')
            
            if pd.notna(institution) and institution != '':
                education_entries.append({
                    'institution': str(institution),
                    'degree': str(degree) if pd.notna(degree) else None,
                    'field_of_study': str(field_of_study) if pd.notna(field_of_study) else None,
                    'start_date': self.parse_date(start_date),
                    'end_date': self.parse_date(end_date),
                    'description': str(description) if pd.notna(description) else None
                })
        
        return education_entries
    
    def extract_experience(self, row: pd.Series) -> List[Dict[str, Any]]:
        """Extract work experience from LinkedIn data"""
        experience_entries = []
        
        # Check for organization data (up to 10 organizations)
        for i in range(1, 11):
            organization_name = row.get(f'organization_{i}', '')
            organization_id = row.get(f'organization_id_{i}', '')
            organization_url = row.get(f'organization_url_{i}', '')
            title = row.get(f'organization_title_{i}', '')
            start_date = row.get(f'organization_start_{i}', '')
            end_date = row.get(f'organization_end_{i}', '')
            description = row.get(f'organization_description_{i}', '')
            location = row.get(f'organization_location_{i}', '')
            website = row.get(f'organization_website_{i}', '')
            domain = row.get(f'organization_domain_{i}', '')
            position_description = row.get(f'position_description_{i}', '')
            
            if pd.notna(organization_name) and organization_name != '':
                experience_entries.append({
                    'organization_name': str(organization_name),
                    'organization_id': str(organization_id) if pd.notna(organization_id) else None,
                    'organization_url': str(organization_url) if pd.notna(organization_url) else None,
                    'title': str(title) if pd.notna(title) else None,
                    'start_date': self.parse_date(start_date),
                    'end_date': self.parse_date(end_date),
                    'description': str(description) if pd.notna(description) else None,
                    'location': str(location) if pd.notna(location) else None,
                    'website': str(website) if pd.notna(website) else None,
                    'domain': str(domain) if pd.notna(domain) else None,
                    'position_description': str(position_description) if pd.notna(position_description) else None
                })
        
        return experience_entries
    
    def calculate_experience_years(self, experience_entries: List[Dict[str, Any]]) -> float:
        """Calculate total experience years from work history"""
        total_years = 0.0
        
        for exp in experience_entries:
            start_date = exp.get('start_date')
            end_date = exp.get('end_date')
            
            if start_date:
                if end_date:
                    # Calculate duration between start and end
                    duration = (end_date - start_date).days / 365.25
                else:
                    # If no end date, calculate from start to current date
                    duration = (date.today() - start_date).days / 365.25
                
                total_years += duration
        
        return round(total_years, 1)
    
    def create_candidate_from_row(self, row: pd.Series) -> Candidate:
        """Create a Candidate object from a CSV row"""
        # Create candidate object with ALL fields from CSV
        candidate = Candidate(
            public_id=str(row.get('public_id', '')) if pd.notna(row.get('public_id', '')) else None,
            member_id=str(row.get('member_id', '')) if pd.notna(row.get('member_id', '')) else None,
            profile_url=str(row.get('profile_url', '')) if pd.notna(row.get('profile_url', '')) else None,
            email=str(row.get('email', '')) if pd.notna(row.get('email', '')) else None,
            full_name=str(row.get('full_name', '')) if pd.notna(row.get('full_name', '')) else None,
            first_name=str(row.get('first_name', '')) if pd.notna(row.get('first_name', '')) else None,
            last_name=str(row.get('last_name', '')) if pd.notna(row.get('last_name', '')) else None,
            original_full_name=str(row.get('original_full_name', '')) if pd.notna(row.get('original_full_name', '')) else None,
            avatar=str(row.get('avatar', '')) if pd.notna(row.get('avatar', '')) else None,
            headline=str(row.get('headline', '')) if pd.notna(row.get('headline', '')) else None,
            location_name=str(row.get('location_name', '')) if pd.notna(row.get('location_name', '')) else None,
            industry=str(row.get('industry', '')) if pd.notna(row.get('industry', '')) else None,
            summary=str(row.get('summary', '')) if pd.notna(row.get('summary', '')) else None,
            address=str(row.get('address', '')) if pd.notna(row.get('address', '')) else None,
            birthday=self.parse_date(row.get('birthday', '')),
            followers=int(row.get('followers', 0)) if pd.notna(row.get('followers', 0)) and str(row.get('followers', 0)).isdigit() else None,
            connections_count=int(row.get('connections_count', 0)) if pd.notna(row.get('connections_count', 0)) and str(row.get('connections_count', 0)).isdigit() else None,
            current_company=str(row.get('current_company', '')) if pd.notna(row.get('current_company', '')) else None,
            current_company_custom=str(row.get('current_company_custom', '')) if pd.notna(row.get('current_company_custom', '')) else None,
            current_company_position=str(row.get('current_company_position', '')) if pd.notna(row.get('current_company_position', '')) else None,
            current_company_custom_position=str(row.get('current_company_custom_position', '')) if pd.notna(row.get('current_company_custom_position', '')) else None,
            current_company_actual_at=self.parse_date(row.get('current_company_actual_at', '')),
            current_company_industry=str(row.get('current_company_industry', '')) if pd.notna(row.get('current_company_industry', '')) else None,
            phone_1=str(row.get('phone_1', '')) if pd.notna(row.get('phone_1', '')) else None,
            phone_type_1=str(row.get('phone_type_1', '')) if pd.notna(row.get('phone_type_1', '')) else None,
            phone_2=str(row.get('phone_2', '')) if pd.notna(row.get('phone_2', '')) else None,
            phone_type_2=str(row.get('phone_type_2', '')) if pd.notna(row.get('phone_type_2', '')) else None,
            messenger_1=str(row.get('messenger_1', '')) if pd.notna(row.get('messenger_1', '')) else None,
            messenger_provider_1=str(row.get('messenger_provider_1', '')) if pd.notna(row.get('messenger_provider_1', '')) else None,
            messenger_2=str(row.get('messenger_2', '')) if pd.notna(row.get('messenger_2', '')) else None,
            messenger_provider_2=str(row.get('messenger_provider_2', '')) if pd.notna(row.get('messenger_provider_2', '')) else None,
            timestamp=datetime.now()
        )
        
        return candidate
    
    def create_education_objects(self, candidate_id: int, education_entries: List[Dict[str, Any]]) -> List[Education]:
        """Create Education objects for a candidate"""
        education_objects = []
        
        for edu in education_entries:
            education = Education(
                candidate_id=candidate_id,
                institution=edu['institution'],
                degree=edu['degree'],
                field_of_study=edu['field_of_study'],
                start_date=edu['start_date'],
                end_date=edu['end_date'],
                description=edu['description']
            )
            education_objects.append(education)
        
        return education_objects
    
    def create_experience_objects(self, candidate_id: int, experience_entries: List[Dict[str, Any]]) -> List[Experience]:
        """Create Experience objects for a candidate"""
        experience_objects = []
        
        for exp in experience_entries:
            experience = Experience(
                candidate_id=candidate_id,
                organization_name=exp['organization_name'],
                organization_id=exp['organization_id'],
                organization_url=exp['organization_url'],
                title=exp['title'],
                start_date=exp['start_date'],
                end_date=exp['end_date'],
                description=exp['description'],
                location=exp['location'],
                website=exp['website'],
                domain=exp['domain'],
                position_description=exp['position_description']
            )
            experience_objects.append(experience)
        
        return experience_objects
    
    def create_skill_objects(self, candidate_id: int, skills: List[str]) -> List[Skill]:
        """Create Skill objects for a candidate"""
        skill_objects = []
        
        for skill in skills:
            skill_obj = Skill(
                candidate_id=candidate_id,
                skill_name=skill,
                proficiency=None  # Not available in LinkedIn data
            )
            skill_objects.append(skill_obj)
        
        return skill_objects
    
    def create_language_objects(self, candidate_id: int, languages: List[str]) -> List[Language]:
        """Create Language objects for a candidate"""
        language_objects = []
        
        for language in languages:
            language_obj = Language(
                candidate_id=candidate_id,
                language_name=language,
                proficiency=None  # Not available in LinkedIn data
            )
            language_objects.append(language_obj)
        
        return language_objects
    
    def create_website_objects(self, candidate_id: int, websites: List[str]) -> List[Website]:
        """Create Website objects for a candidate"""
        website_objects = []
        
        for i, website in enumerate(websites):
            website_obj = Website(
                candidate_id=candidate_id,
                website_url=website,
                website_type=f"website_{i+1}"  # website_1, website_2, etc.
            )
            website_objects.append(website_obj)
        
        return website_objects
    
    def process_row(self, row: pd.Series) -> bool:
        """Process a single row from the CSV"""
        try:
            # Create candidate
            candidate = self.create_candidate_from_row(row)
            self.db.add(candidate)
            self.db.flush()  # Get the candidate_id
            
            # Extract and create education entries
            education_entries = self.extract_education(row)
            education_objects = self.create_education_objects(candidate.candidate_id, education_entries)
            for edu in education_objects:
                self.db.add(edu)
            
            # Extract and create experience entries
            experience_entries = self.extract_experience(row)
            experience_objects = self.create_experience_objects(candidate.candidate_id, experience_entries)
            for exp in experience_objects:
                self.db.add(exp)
            
            # Extract and create skills
            skills_data = row.get('skills', '')
            skills = self.extract_skills(skills_data)
            skill_objects = self.create_skill_objects(candidate.candidate_id, skills)
            for skill in skill_objects:
                self.db.add(skill)
            
            # Extract and create languages
            languages_data = row.get('languages', '')
            languages = self.extract_languages(languages_data)
            language_objects = self.create_language_objects(candidate.candidate_id, languages)
            for language in language_objects:
                self.db.add(language)
            
            # Extract and create websites
            website_1 = row.get('website_1', '')
            website_2 = row.get('website_2', '')
            website_3 = row.get('website_3', '')
            websites = []
            if pd.notna(website_1) and website_1 != '':
                websites.append(str(website_1))
            if pd.notna(website_2) and website_2 != '':
                websites.append(str(website_2))
            if pd.notna(website_3) and website_3 != '':
                websites.append(str(website_3))
            
            website_objects = self.create_website_objects(candidate.candidate_id, websites)
            for website in website_objects:
                self.db.add(website)
            
            self.db.commit()
            logger.info(f"Successfully processed candidate: {candidate.full_name}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error processing row: {e}")
            return False
    
    def process_all(self) -> Dict[str, int]:
        """Process all rows in the CSV file"""
        if not self.load_csv():
            return {'success': 0, 'failed': 0, 'total': 0}
        
        success_count = 0
        failed_count = 0
        total_count = len(self.df)
        
        logger.info(f"Starting to process {total_count} candidates...")
        
        for index, row in self.df.iterrows():
            logger.info(f"Processing candidate {index + 1}/{total_count}")
            
            if self.process_row(row):
                success_count += 1
            else:
                failed_count += 1
        
        self.db.close()
        
        results = {
            'success': success_count,
            'failed': failed_count,
            'total': total_count
        }
        
        logger.info(f"Processing complete. Success: {success_count}, Failed: {failed_count}, Total: {total_count}")
        return results
