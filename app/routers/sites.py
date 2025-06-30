# app/api/sites.py
import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from datetime import datetime
from typing import List

from app.models.site import SitePhoto, SiteDocument

UPLOAD_DIR = "app/uploads/sites"

router = APIRouter(prefix="/sites", tags=["sites"])

# Helper pour générer l'URL publique (adapte si besoin !)
def public_url(file_path: str) -> str:
    # En prod, remplace "localhost:8000" par ton nom de domaine
    return f"http://localhost:8000/static/{file_path}"

@router.post("/{site_id}/photos", response_model=SitePhoto)
async def upload_photo(site_id: str, file: UploadFile = File(...)):
    site_photo_dir = os.path.join(UPLOAD_DIR, site_id, "photos")
    os.makedirs(site_photo_dir, exist_ok=True)
    filename = f"{int(datetime.now().timestamp())}_{file.filename}"
    file_path = os.path.join(site_photo_dir, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    photo = SitePhoto(
        filename=filename,
        fileUrl=public_url(f"sites/{site_id}/photos/{filename}"),
        uploadedAt=datetime.now().isoformat()
    )
    return photo

@router.get("/{site_id}/photos", response_model=List[SitePhoto])
async def list_photos(site_id: str):
    site_photo_dir = os.path.join(UPLOAD_DIR, site_id, "photos")
    if not os.path.exists(site_photo_dir):
        return []
    files = os.listdir(site_photo_dir)
    files.sort(reverse=True)
    return [
        SitePhoto(
            filename=filename,
            fileUrl=public_url(f"sites/{site_id}/photos/{filename}"),
            uploadedAt=datetime.fromtimestamp(os.path.getmtime(os.path.join(site_photo_dir, filename))).isoformat()
        )
        for filename in files
    ]

@router.delete("/{site_id}/photos/{filename}")
async def delete_photo(site_id: str, filename: str):
    site_photo_dir = os.path.join(UPLOAD_DIR, site_id, "photos")
    file_path = os.path.join(site_photo_dir, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"detail": "Deleted"}
    raise HTTPException(status_code=404, detail="Not found")

# --- Documents (très similaire) ---

@router.post("/{site_id}/documents", response_model=SiteDocument)
async def upload_document(site_id: str, file: UploadFile = File(...)):
    site_doc_dir = os.path.join(UPLOAD_DIR, site_id, "documents")
    os.makedirs(site_doc_dir, exist_ok=True)
    filename = f"{int(datetime.now().timestamp())}_{file.filename}"
    file_path = os.path.join(site_doc_dir, filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    doc = SiteDocument(
        filename=filename,
        fileUrl=public_url(f"sites/{site_id}/documents/{filename}"),
        uploadedAt=datetime.now().isoformat()
    )
    return doc

@router.get("/{site_id}/documents", response_model=List[SiteDocument])
async def list_documents(site_id: str):
    site_doc_dir = os.path.join(UPLOAD_DIR, site_id, "documents")
    if not os.path.exists(site_doc_dir):
        return []
    files = os.listdir(site_doc_dir)
    files.sort(reverse=True)
    return [
        SiteDocument(
            filename=filename,
            fileUrl=public_url(f"sites/{site_id}/documents/{filename}"),
            uploadedAt=datetime.fromtimestamp(os.path.getmtime(os.path.join(site_doc_dir, filename))).isoformat()
        )
        for filename in files
    ]

@router.delete("/{site_id}/documents/{filename}")
async def delete_document(site_id: str, filename: str):
    site_doc_dir = os.path.join(UPLOAD_DIR, site_id, "documents")
    file_path = os.path.join(site_doc_dir, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"detail": "Deleted"}
    raise HTTPException(status_code=404, detail="Not found")
