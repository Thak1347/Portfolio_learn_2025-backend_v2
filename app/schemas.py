from pydantic import BaseModel, ConfigDict, Field  # Add Field import here
from datetime import datetime
from typing import Optional, List

# Auth
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

# User
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Post
class PostBase(BaseModel):
    title: str
    content: str
    tags: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None

class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# Certificate
class CertificateBase(BaseModel):
    title: str
    issuer: str
    date: str

class CertificateCreate(CertificateBase):
    pass

class Certificate(CertificateBase):
    id: int
    image_url: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class CertificateUpdate(BaseModel):
    title: Optional[str] = None
    issuer: Optional[str] = None
    date: Optional[str] = None

# Skill Schemas
class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None
    proficiency: Optional[int] = Field(None, ge=0, le=100)
    icon_url: Optional[str] = None
    color: Optional[str] = None
    order: Optional[int] = 0
    is_featured: Optional[bool] = False

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    proficiency: Optional[int] = Field(None, ge=0, le=100)
    icon_url: Optional[str] = None
    color: Optional[str] = None
    order: Optional[int] = None
    is_featured: Optional[bool] = None

class Skill(SkillBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)