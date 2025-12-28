from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.database import engine, Base
from app.routers import auth, posts, certificates, skills
from app.auth import create_default_admin

# Create database tables
Base.metadata.create_all(bind=engine)

# Create upload directories if they don't exist
os.makedirs("app/uploads/posts", exist_ok=True)
os.makedirs("app/uploads/certificates", exist_ok=True)
os.makedirs("app/uploads/skills", exist_ok=True)  # Add skills directory

app = FastAPI(title="Pithak Chhorn Portfolio API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/uploads"), name="static")

# Include routers
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(posts.router, prefix="/api", tags=["posts"])
app.include_router(certificates.router, prefix="/api", tags=["certificates"])
app.include_router(skills.router, prefix="/api", tags=["skills"])

@app.on_event("startup")
async def startup_event():
    # Create default admin user
    await create_default_admin()
    # Seed initial skills
    await seed_initial_skills()

@app.get("/")
async def root():
    return {"message": "Welcome to Pithak Chhorn Portfolio API"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

async def seed_initial_skills():
    """Seed database with initial skills if empty"""
    from app.database import SessionLocal
    from app.models import Skill
    
    db = SessionLocal()
    try:
        skill_count = db.query(Skill).count()
        if skill_count == 0:
            initial_skills = [
                Skill(name="Python", category="Programming", proficiency=90, color="#3776AB", order=1, is_featured=True),
                Skill(name="JavaScript", category="Programming", proficiency=85, color="#F7DF1E", order=2, is_featured=True),
                Skill(name="FastAPI", category="Framework", proficiency=80, color="#009688", order=3, is_featured=True),
                Skill(name="React", category="Framework", proficiency=75, color="#61DAFB", order=4, is_featured=True),
                Skill(name="SQL", category="Database", proficiency=85, color="#4479A1", order=5),
                Skill(name="Git", category="Tool", proficiency=80, color="#F05032", order=6),
                Skill(name="Docker", category="Tool", proficiency=70, color="#2496ED", order=7),
                Skill(name="HTML/CSS", category="Web", proficiency=95, color="#E34F26", order=8),
                Skill(name="TypeScript", category="Programming", proficiency=70, color="#3178C6", order=9),
                Skill(name="PostgreSQL", category="Database", proficiency=75, color="#4169E1", order=10),
            ]
            db.add_all(initial_skills)
            db.commit()
            print("✓ Initial skills seeded successfully")
        else:
            print(f"✓ Database already has {skill_count} skills")
    except Exception as e:
        print(f"✗ Error seeding skills: {e}")
    finally:
        db.close()