import os
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
import shutil

from app.database import get_db
from app.deps import get_current_active_user
from app.models import User, Post
from app.schemas import Post as PostSchema, PostCreate, PostUpdate

router = APIRouter()

@router.get("/posts", response_model=List[PostSchema])
async def read_posts(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Post)
    if category:
        query = query.filter(Post.category == category)
    posts = query.order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    return posts

@router.get("/posts/{post_id}", response_model=PostSchema)
async def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/posts", response_model=PostSchema)
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    tags: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    image_url = None
    if image:
        # Save uploaded image
        file_location = f"app/uploads/posts/{image.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(image.file, file_object)
        image_url = f"/static/posts/{image.filename}"
    
    db_post = Post(
        title=title,
        content=content,
        tags=tags,
        category=category,
        image_url=image_url
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.put("/posts/{post_id}", response_model=PostSchema)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    update_data = post_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_post, field, value)
    
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Delete associated image file if exists
    if db_post.image_url:
        image_path = f"app{db_post.image_url}"
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}