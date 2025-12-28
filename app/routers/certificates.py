import os
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
import shutil
import secrets
from pathlib import Path

from app.database import get_db
from app.deps import get_current_active_user
from app.models import User, Certificate
from app.schemas import Certificate as CertificateSchema, CertificateCreate, CertificateUpdate

router = APIRouter()

@router.get("/certificates", response_model=List[CertificateSchema])
async def read_certificates(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    certificates = db.query(Certificate).order_by(Certificate.created_at.desc()).offset(skip).limit(limit).all()
    return certificates

@router.get("/certificates/{certificate_id}", response_model=CertificateSchema)
async def read_certificate(
    certificate_id: int,
    db: Session = Depends(get_db)
):
    certificate = db.query(Certificate).filter(Certificate.id == certificate_id).first()
    if certificate is None:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return certificate

@router.post("/certificates", response_model=CertificateSchema)
async def create_certificate(
    title: str = Form(...),
    issuer: str = Form(...),
    date: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Validate file type
    allowed_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.pdf', '.webp')
    if not image.filename.lower().endswith(allowed_extensions):
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Generate unique filename to avoid conflicts
    file_extension = Path(image.filename).suffix
    unique_filename = f"{secrets.token_hex(8)}_{title.replace(' ', '_')[:50]}{file_extension}"
    
    # Save uploaded image
    upload_dir = "app/uploads/certificates"
    os.makedirs(upload_dir, exist_ok=True)
    file_location = f"{upload_dir}/{unique_filename}"
    
    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(image.file, file_object)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    image_url = f"/static/certificates/{unique_filename}"
    
    db_certificate = Certificate(
        title=title,
        issuer=issuer,
        date=date,
        image_url=image_url
    )
    db.add(db_certificate)
    db.commit()
    db.refresh(db_certificate)
    return db_certificate

@router.put("/certificates/{certificate_id}", response_model=CertificateSchema)
async def update_certificate(
    certificate_id: int,
    title: Optional[str] = Form(None),
    issuer: Optional[str] = Form(None),
    date: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_certificate = db.query(Certificate).filter(Certificate.id == certificate_id).first()
    if db_certificate is None:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    # Update text fields if provided
    if title is not None:
        db_certificate.title = title
    if issuer is not None:
        db_certificate.issuer = issuer
    if date is not None:
        db_certificate.date = date
    
    # Handle image update if provided
    if image:
        # Validate file type
        allowed_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.pdf', '.webp')
        if not image.filename.lower().endswith(allowed_extensions):
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        # Generate unique filename
        file_extension = Path(image.filename).suffix
        unique_filename = f"{secrets.token_hex(8)}_{db_certificate.title.replace(' ', '_')[:50]}{file_extension}"
        
        # Delete old image if exists
        if db_certificate.image_url:
            old_image_path = f"app{db_certificate.image_url}"
            if os.path.exists(old_image_path):
                try:
                    os.remove(old_image_path)
                except Exception as e:
                    print(f"Warning: Could not delete old image: {str(e)}")
        
        # Save new image
        upload_dir = "app/uploads/certificates"
        os.makedirs(upload_dir, exist_ok=True)
        file_location = f"{upload_dir}/{unique_filename}"
        
        try:
            with open(file_location, "wb+") as file_object:
                shutil.copyfileobj(image.file, file_object)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
        
        db_certificate.image_url = f"/static/certificates/{unique_filename}"
    
    db.commit()
    db.refresh(db_certificate)
    return db_certificate

@router.patch("/certificates/{certificate_id}", response_model=CertificateSchema)
async def partial_update_certificate(
    certificate_id: int,
    certificate_update: CertificateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_certificate = db.query(Certificate).filter(Certificate.id == certificate_id).first()
    if db_certificate is None:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    # Update only provided fields
    update_data = certificate_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_certificate, field, value)
    
    db.commit()
    db.refresh(db_certificate)
    return db_certificate

@router.delete("/certificates/{certificate_id}")
async def delete_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_certificate = db.query(Certificate).filter(Certificate.id == certificate_id).first()
    if db_certificate is None:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    # Delete associated image file
    if db_certificate.image_url:
        image_path = f"app{db_certificate.image_url}"
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except Exception as e:
                print(f"Warning: Could not delete image file: {str(e)}")
    
    db.delete(db_certificate)
    db.commit()
    return {"message": "Certificate deleted successfully"}