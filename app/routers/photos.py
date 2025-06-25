from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
from datetime import datetime
from uuid import uuid4

router = APIRouter()

UPLOAD_DIR = "app/uploads/sites"

@router.post("/sites/{site_id}/photos")
async def upload_photo(site_id: str, file: UploadFile = File(...)):
    # Créer le dossier du site si besoin
    site_dir = os.path.join(UPLOAD_DIR, site_id)
    os.makedirs(site_dir, exist_ok=True)
    # Horodatage et nommage unique
    ext = os.path.splitext(file.filename)[1]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    new_name = f"{timestamp}_{uuid4().hex}{ext}"
    file_path = os.path.join(site_dir, new_name)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    # Retourne l'URL publique (à adapter selon ton serveur/nginx/etc)
    file_url = f"/static/sites/{site_id}/{new_name}"
    uploaded_at = datetime.now().isoformat()
    return {"fileUrl": file_url, "uploadedAt": uploaded_at}
