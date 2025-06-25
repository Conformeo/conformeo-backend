from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.site import Site
from app.models.site_photo import SitePhoto
from datetime import datetime
import os, shutil

router = APIRouter()

@router.post("/sites/{site_id}/photo")
def upload_site_photo(site_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Vérifier que le site existe
    site = db.query(Site).filter_by(id=site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Chantier introuvable")

    # Crée le dossier si besoin
    upload_dir = f"uploads/sites/{site_id}"
    os.makedirs(upload_dir, exist_ok=True)
    # Chemin du fichier
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_url = f"/uploads/sites/{site_id}/{file.filename}"

    # Enregistre en base
    photo = SitePhoto(
        site_id=site_id,
        file_url=file_url,
        uploaded_at=datetime.utcnow(),
        uploaded_by="admin",
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return {
        "id": photo.id,
        "fileUrl": photo.file_url,
        "uploadedAt": photo.uploaded_at,
        "uploadedBy": photo.uploaded_by,
    }

@router.get("/sites/{site_id}/photos")
def list_site_photos(site_id: int, db: Session = Depends(get_db)):
    photos = db.query(SitePhoto).filter_by(site_id=site_id).order_by(SitePhoto.uploaded_at.desc()).all()
    return [
        {
            "id": p.id,
            "fileUrl": p.file_url,
            "uploadedAt": p.uploaded_at,
            "uploadedBy": p.uploaded_by,
        }
        for p in photos
    ]
