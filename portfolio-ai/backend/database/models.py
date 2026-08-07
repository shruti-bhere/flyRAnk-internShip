from sqlalchemy import Column, Integer, String, Text, DateTime, ARRAY
from datetime import datetime, timezone
from backend.database.connection import Base

class User(Base):
    """
    Stores system administrator authentication credentials.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Project(Base):
    """
    Stores curated, high-impact project descriptions managed via the Admin Panel.
    """
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    tech_stack = Column(ARRAY(String), nullable=False)  # Array type to host tag filters
    live_link = Column(String(255), nullable=True)
    github_link = Column(String(255), nullable=True)
    category = Column(String(50), nullable=False, index=True) # e.g., "AI", "Backend", "RAG"
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class VisitorLog(Base):
    """
    Captures anonymized user interaction and traffic metrics for telemetry analysis.
    """
    __tablename__ = "visitor_logs"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(45), nullable=False)
    device = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    active_section = Column(String(50), nullable=False) # Tracks last active navigation anchor
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))