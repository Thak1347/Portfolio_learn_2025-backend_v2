from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func  # Import func from sqlalchemy

from app.database import get_db
from app.deps import get_current_active_user
from app.models import User, Skill
from app.schemas import Skill as SkillSchema, SkillCreate, SkillUpdate

router = APIRouter()

@router.get("/skills", response_model=List[SkillSchema])
async def read_skills(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[str] = None,
    featured: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Get all skills with optional filtering
    """
    query = db.query(Skill)
    
    # Apply filters
    if category:
        query = query.filter(Skill.category == category)
    
    if featured is not None:
        query = query.filter(Skill.is_featured == featured)
    
    # Apply sorting and pagination
    skills = query.order_by(Skill.order.asc(), Skill.name.asc()).offset(skip).limit(limit).all()
    return skills

@router.get("/skills/categories", response_model=List[str])
async def read_skill_categories(db: Session = Depends(get_db)):
    """
    Get distinct skill categories
    """
    categories = db.query(Skill.category).distinct().all()
    return [cat[0] for cat in categories if cat[0]]

@router.get("/skills/{skill_id}", response_model=SkillSchema)
async def read_skill(skill_id: int, db: Session = Depends(get_db)):
    """
    Get a specific skill by ID
    """
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@router.post("/skills", response_model=SkillSchema)
async def create_skill(
    skill_data: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new skill (Admin only)
    """
    # Check if skill with same name already exists
    existing_skill = db.query(Skill).filter(Skill.name == skill_data.name).first()
    if existing_skill:
        raise HTTPException(
            status_code=400,
            detail="Skill with this name already exists"
        )
    
    db_skill = Skill(**skill_data.model_dump())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

@router.put("/skills/{skill_id}", response_model=SkillSchema)
async def update_skill(
    skill_id: int,
    skill_update: SkillUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a skill (Admin only)
    """
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if db_skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    # Check name uniqueness if name is being updated
    if skill_update.name and skill_update.name != db_skill.name:
        existing_skill = db.query(Skill).filter(
            Skill.name == skill_update.name,
            Skill.id != skill_id
        ).first()
        if existing_skill:
            raise HTTPException(
                status_code=400,
                detail="Skill with this name already exists"
            )
    
    # Update fields
    update_data = skill_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_skill, field, value)
    
    db.commit()
    db.refresh(db_skill)
    return db_skill

@router.delete("/skills/{skill_id}")
async def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a skill (Admin only)
    """
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if db_skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    db.delete(db_skill)
    db.commit()
    return {"message": "Skill deleted successfully"}

@router.get("/skills/stats/category-distribution")
async def get_category_distribution(db: Session = Depends(get_db)):
    """
    Get skill distribution by category
    """
    result = db.query(
        Skill.category,
        func.count(Skill.id).label('count')  # Use func from sqlalchemy
    ).group_by(Skill.category).all()
    
    distribution = [
        {"category": category, "count": count}
        for category, count in result
        if category  # Exclude null categories
    ]
    return distribution

@router.get("/skills/stats/proficiency-levels")
async def get_proficiency_levels(db: Session = Depends(get_db)):
    """
    Get skill proficiency statistics
    """
    stats = db.query(
        func.avg(Skill.proficiency).label('average'),
        func.max(Skill.proficiency).label('max'),
        func.min(Skill.proficiency).label('min'),
        func.count(Skill.id).label('total')
    ).filter(Skill.proficiency.isnot(None)).first()
    
    return {
        "average_proficiency": round(stats.average or 0, 2),
        "max_proficiency": stats.max or 0,
        "min_proficiency": stats.min or 100,
        "total_skills": stats.total or 0
    }

@router.get("/skills/featured", response_model=List[SkillSchema])
async def get_featured_skills(
    limit: int = Query(10, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Get featured skills for portfolio showcase"""
    skills = db.query(Skill).filter(
        Skill.is_featured == True
    ).order_by(
        Skill.order.asc()
    ).limit(limit).all()
    return skills