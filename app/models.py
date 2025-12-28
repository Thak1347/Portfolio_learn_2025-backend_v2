from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(String)  # Comma-separated tags
    category = Column(String, index=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Certificate(Base):
    __tablename__ = "certificates"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    issuer = Column(String, nullable=False)
    date = Column(String)  # Store as string for flexibility
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String, index=True)  # e.g., "Programming", "Framework", "Tool", "Database"
    proficiency = Column(Integer)  # 1-100 percentage
    icon_url = Column(String, nullable=True)  # URL to skill icon/image
    color = Column(String, nullable=True)  # Hex color for UI
    order = Column(Integer, default=0)  # For sorting
    is_featured = Column(Boolean, default=False)  # Highlight in portfolio
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())