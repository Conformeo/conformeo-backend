# app/routers/sites.py
import os, uuid
from datetime import datetime
from typing import Dict, List

from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.site import Site, SitePhoto, SiteDocument   # ⬅️ 3 modèles

# ──────────────────────────────────────────────
#   CONFIG
# ──────────────────────────────────────────────
UPLOAD_DIR = "app/uploads/sites"
router     = APIRouter(prefix="/sites", tags=["sites"])

def public_url(path: str) -> str:
    """Construit une URL publique pour servir le fichier statique."""
    return f"http://localhost:8000/static/{path}"

# ──────────────────────────────────────────────
#   MOCK (remplace par une BDD / ORM plus tard)
# ──────────────────────────────────────────────
_sites_db: Dict[str, Site] = {
    "1": Site(id="1", name="Chantier A", address="12 rue du Parc",
              city="Paris", zipCode="75000", score=90),
    "2": Site(id="2", name="Chantier B", address="48 rue du Port",
              city="Lyon",  zipCode="69000", score=88),
}

# ──────────────────────────────────────────────
#   C R U D   S I T E S
# ──────────────────────────────────────────────
@router.get("", response_model=List[Site])
async def list_sites():
    return list(_sites_db.values())

@router.post("", response_model=Site, status_code=201)
async def create_site(site: Site):
    if site.id in _sites_db:
        raise HTTPException(400, "Site ID already exists")
    _sites_db[site.id] = site
    return site

@router.get("/{site_id}", response_model=Site)
async def get_site(site_id: str):
    site = _sites_db.get(site_id)
    if not site:
        raise HTTPException(404, "Site not found")
    return site

@router.put("/{site_id}", response_model=Site)
async def update_site(site_id: str, site: Site):
    if site_id not in _sites_db:
        raise HTTPException(404, "Site not found")
    _sites_db[site_id] = site
    return site

@router.delete("/{site_id}", status_code=204)
async def delete_site(site_id: str):
    if site_id not in _sites_db:
        raise HTTPException(404, "Site not found")
    _sites_db.pop(site_id)
    return None

# ──────────────────────────────────────────────
#   P H O T O S
# ──────────────────────────────────────────────
@router.post("/{site_id}/photos", response_model=SitePhoto)
async def upload_photo(site_id: str, file: UploadFile = File(...)):
    folder = os.path.join(UPLOAD_DIR, site_id, "photos")
    os.makedirs(folder, exist_ok=True)

    filename  = f"{int(datetime.now().timestamp())}_{file.filename}"
    file_path = os.path.join(folder, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return SitePhoto(
        filename   = filename,
        fileUrl    = public_url(f"sites/{site_id}/photos/{filename}"),
        uploadedAt = datetime.now().isoformat()
    )

@router.get("/{site_id}/photos", response_model=List[SitePhoto])
async def list_photos(site_id: str):
    folder = os.path.join(UPLOAD_DIR, site_id, "photos")
    if not os.path.exists(folder):
        return []

    files = sorted(os.listdir(folder), reverse=True)
    return [
        SitePhoto(
            filename   = f,
            fileUrl    = public_url(f"sites/{site_id}/photos/{f}"),
            uploadedAt = datetime.fromtimestamp(
                os.path.getmtime(os.path.join(folder, f))
            ).isoformat()
        )
        for f in files
    ]

@router.delete("/{site_id}/photos/{filename}")
async def delete_photo(site_id: str, filename: str):
    path = os.path.join(UPLOAD_DIR, site_id, "photos", filename)
    if not os.path.exists(path):
        raise HTTPException(404, "Not found")

    os.remove(path)
    return {"detail": "Deleted"}

# ──────────────────────────────────────────────
#   D O C U M E N T S
# ──────────────────────────────────────────────
@router.post("/{site_id}/documents", response_model=SiteDocument)
async def upload_document(site_id: str, file: UploadFile = File(...)):
    folder = os.path.join(UPLOAD_DIR, site_id, "documents")
    os.makedirs(folder, exist_ok=True)

    filename  = f"{int(datetime.now().timestamp())}_{file.filename}"
    file_path = os.path.join(folder, filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return SiteDocument(
        filename   = filename,
        fileUrl    = public_url(f"sites/{site_id}/documents/{filename}"),
        uploadedAt = datetime.now().isoformat()
    )

@router.get("/{site_id}/documents", response_model=List[SiteDocument])
async def list_documents(site_id: str):
    folder = os.path.join(UPLOAD_DIR, site_id, "documents")
    if not os.path.exists(folder):
        return []

    files = sorted(os.listdir(folder), reverse=True)
    return [
        SiteDocument(
            filename   = f,
            fileUrl    = public_url(f"sites/{site_id}/documents/{f}"),
            uploadedAt = datetime.fromtimestamp(
                os.path.getmtime(os.path.join(folder, f))
            ).isoformat()
        )
        for f in files
    ]

@router.delete("/{site_id}/documents/{filename}")
async def delete_document(site_id: str, filename: str):
    path = os.path.join(UPLOAD_DIR, site_id, "documents", filename)
    if not os.path.exists(path):
        raise HTTPException(404, "Not found")

    os.remove(path)
    return {"detail": "Deleted"}
