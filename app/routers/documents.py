from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_service import save_document, list_documents, delete_document

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/{site_id}/upload")
async def upload_document(site_id: str, file: UploadFile = File(...)):
    doc = save_document(site_id, file)
    return doc

@router.get("/{site_id}")
async def get_documents(site_id: str):
    return list_documents(site_id)

@router.delete("/{filename}")
async def remove_document(filename: str):
    if delete_document(filename):
        return {"ok": True}
    raise HTTPException(status_code=404, detail="Document not found")
