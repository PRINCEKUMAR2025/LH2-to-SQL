from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Double, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from config import DATABASE_URL_WITH_SSL

Base = declarative_base()

class Candidate(Base):
    __tablename__ = 'candidate'
    
    candidate_id = Column(Integer, primary_key=True, autoincrement=True)
    public_id = Column(String(255))
    member_id = Column(String(255))
    profile_url = Column(Text)
    email = Column(Text)
    full_name = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    original_full_name = Column(String(255))
    avatar = Column(Text)
    headline = Column(Text)
    location_name = Column(String(255))
    industry = Column(String(255))
    summary = Column(Text)
    address = Column(Text)
    birthday = Column(Date)
    followers = Column(Integer)
    connections_count = Column(Integer)
    current_company = Column(String(255))
    current_company_custom = Column(String(255))
    current_company_position = Column(String(255))
    current_company_custom_position = Column(String(255))
    current_company_actual_at = Column(Date)
    current_company_industry = Column(String(255))
    phone_1 = Column(String(50))
    phone_type_1 = Column(String(50))
    phone_2 = Column(String(50))
    phone_type_2 = Column(String(50))
    messenger_1 = Column(String(255))
    messenger_provider_1 = Column(String(100))
    messenger_2 = Column(String(255))
    messenger_provider_2 = Column(String(100))
    timestamp = Column(DateTime, default=datetime.now)
    
    # Relationships
    educations = relationship("Education", back_populates="candidate")
    experiences = relationship("Experience", back_populates="candidate")
    projects = relationship("Project", back_populates="candidate")
    skills = relationship("Skill", back_populates="candidate")
    languages = relationship("Language", back_populates="candidate")
    websites = relationship("Website", back_populates="candidate")
    years_of_experience = relationship("YearsOfExperience", back_populates="candidate")

class Education(Base):
    __tablename__ = 'education'
    
    education_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey('candidate.candidate_id'))
    institution = Column(String(255))
    degree = Column(String(255))
    field_of_study = Column(String(255))
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text)
    
    # Relationship
    candidate = relationship("Candidate", back_populates="educations")

class Experience(Base):
    __tablename__ = 'experience'
    
    experience_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey('candidate.candidate_id'))
    organization_name = Column(String(255))
    organization_id = Column(String(255))
    organization_url = Column(Text)
    title = Column(String(255))
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text)
    location = Column(String(255))
    website = Column(Text)
    domain = Column(String(255))
    position_description = Column(Text)
    
    # Relationship
    candidate = relationship("Candidate", back_populates="experiences")

class Project(Base):
    __tablename__ = 'projects'
    
    project_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey('candidate.candidate_id'))
    project_name = Column(String(255))
    description = Column(Text)
    technologies = Column(Text)
    duration = Column(String(100))
    
    # Relationship
    candidate = relationship("Candidate", back_populates="projects")

class Skill(Base):
    __tablename__ = 'skills'
    
    skill_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey('candidate.candidate_id'))
    skill_name = Column(String(255))
    proficiency = Column(String(100))
    
    # Relationship
    candidate = relationship("Candidate", back_populates="skills")

class Language(Base):
    __tablename__ = 'languages'
    
    language_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey('candidate.candidate_id'))
    language_name = Column(String(255))
    proficiency = Column(String(100))
    
    # Relationship
    candidate = relationship("Candidate", back_populates="languages")

class Website(Base):
    __tablename__ = 'websites'
    
    website_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey('candidate.candidate_id'))
    website_url = Column(Text)
    website_type = Column(String(100))
    
    # Relationship
    candidate = relationship("Candidate", back_populates="websites")

class YearsOfExperience(Base):
    __tablename__ = 'yearofexp'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey('candidate.candidate_id'))
    total_years_experience = Column(Double)
    calculated_date = Column(DateTime, default=datetime.now)
    
    # Relationship
    candidate = relationship("Candidate", back_populates="years_of_experience")

# Create engine and session
engine = create_engine(DATABASE_URL_WITH_SSL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
