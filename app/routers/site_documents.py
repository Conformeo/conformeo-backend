# app/api/endpoints/site_documents.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.site_document import SiteDocument
from app.models.site_document import SiteDocument as SiteDocumentModel
from app.db.session import SessionLocal
import shutil, os, uuid
from starlette.responses import FileResponse

router = APIRouter()

UPLOAD_ROOT = "app/uploads/sites"

@router.post("/sites/{site_id}/documents", response_model=SiteDocument)
async def upload_document(site_id: str, file: UploadFile = File(...)):
    os.makedirs(f"{UPLOAD_ROOT}/{site_id}", exist_ok=True)
    filename = f"{uuid.uuid4()}_{file.filename}"
    path = f"{UPLOAD_ROOT}/{site_id}/{filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    file_url = f"/static/sites/{site_id}/{filename}"

    # Enregistre en base (ici à adapter à ton CRUD)
    db = SessionLocal()
    doc = SiteDocumentModel(site_id=site_id, filename=filename, file_url=file_url, type="doc")
    db.add(doc)
    db.commit()
    db.refresh(doc)
    db.close()
    return doc

@router.get("/sites/{site_id}/documents", response_model=list[SiteDocument])
def list_documents(site_id: str):
    db = SessionLocal()
    docs = db.query(SiteDocumentModel).filter_by(site_id=site_id).all()
    db.close()
    return docs

@router.delete("/sites/documents/{filename}")
def delete_document(filename: str):
    db = SessionLocal()
    doc = db.query(SiteDocumentModel).filter_by(filename=filename).first()
    if not doc:
        db.close()
        raise HTTPException(status_code=404, detail="Document not found")
    # Supprime le fichier physique
    try:
        os.remove(f"{UPLOAD_ROOT}/{doc.site_id}/{filename}")
    except FileNotFoundError:
        pass
    db.delete(doc)
    db.commit()
    db.close()
    return {"ok": True}
