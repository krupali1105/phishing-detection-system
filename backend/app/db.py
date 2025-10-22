"""
Database configuration and models for logging predictions.
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./phishing_detection.db")

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class
Base = declarative_base()

class PredictionLog(Base):
    """Model for logging prediction results."""
    
    __tablename__ = "prediction_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    text = Column(String, nullable=True)
    prediction = Column(String, index=True)  # "Phishing" or "Legitimate"
    confidence = Column(Float)
    model_type = Column(String)  # "url", "text", or "hybrid"
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)

class URLBlacklist(Base):
    """Model for maintaining URL blacklist."""
    
    __tablename__ = "url_blacklist"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    domain = Column(String, index=True)
    is_phishing = Column(Boolean, default=True)
    confidence = Column(Float)
    source = Column(String)  # "manual", "model", "external_api"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AnalyticsData(Base):
    """Model for storing analytics data."""
    
    __tablename__ = "analytics_data"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)
    total_predictions = Column(Integer, default=0)
    phishing_count = Column(Integer, default=0)
    legitimate_count = Column(Integer, default=0)
    avg_confidence = Column(Float, default=0.0)

def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables on import
create_tables()
