from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import secrets
import hashlib

from app.database import SessionLocal
from app.models import User
from app.schemas import TokenData

# JWT Configuration
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Try to use bcrypt, fallback to SHA256 if it fails
try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    BCYPT_AVAILABLE = True
except ImportError:
    BCYPT_AVAILABLE = False
    pwd_context = None

def verify_password(plain_password, hashed_password):
    if hashed_password.startswith("sha256$"):
        # Handle our fallback SHA256 hash
        stored_hash = hashed_password.split("$", 1)[1]
        computed_hash = hashlib.sha256(plain_password.encode()).hexdigest()
        return secrets.compare_digest(stored_hash, computed_hash)
    elif BCYPT_AVAILABLE and pwd_context:
        # Handle bcrypt hash
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except:
            return False
    return False

def get_password_hash(password):
    # Truncate password if too long for bcrypt
    if len(password) > 72:
        password = password[:72]
    
    if BCYPT_AVAILABLE and pwd_context:
        try:
            return pwd_context.hash(password)
        except Exception as e:
            print(f"Warning: bcrypt failed, using SHA256 fallback: {e}")
    
    # Fallback to SHA256
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return f"sha256${password_hash}"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

async def authenticate_user(db: Session, username: str, password: str):
    user = await get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
    except JWTError:
        return None
    return token_data

async def create_default_admin():
    db = SessionLocal()
    try:
        admin_user = await get_user(db, "admin")
        if not admin_user:
            hashed_password = get_password_hash("admin123")
            admin_user = User(
                username="admin",
                hashed_password=hashed_password,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("✓ Default admin user created: username='admin', password='admin123'")
        else:
            print("✓ Admin user already exists")
    except Exception as e:
        print(f"✗ Error creating admin user: {e}")
    finally:
        db.close()