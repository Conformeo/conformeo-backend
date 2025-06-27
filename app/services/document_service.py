import os
import shutil
from uuid import uuid4
from datetime import datetime

UPLOAD_DIR = "app/uploads/documents"

def save_document(site_id: str, file) -> dict:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filename = f"{site_id}_{uuid4().hex}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {
        "id": uuid4().hex,
        "site_id": site_id,
        "filename": file.filename,
        "file_url": f"/static/documents/{filename}",
        "uploaded_at": datetime.utcnow()
    }

def list_documents(site_id: str) -> list:
    # Ici, il faudrait normalement stocker la meta en base de données.
    # Pour MVP, on lit le dossier
    docs = []
    for fname in os.listdir(UPLOAD_DIR):
        if fname.startswith(site_id + "_"):
            docs.append({
                "id": fname,
                "site_id": site_id,
                "filename": fname.split("_", 2)[-1],
                "file_url": f"/static/documents/{fname}",
                "uploaded_at": datetime.utcnow()  # Option simplifiée
            })
    return docs

def delete_document(filename: str):
    path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False
