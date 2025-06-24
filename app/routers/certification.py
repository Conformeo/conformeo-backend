# app/routers/certifications.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.certification import Certification

router = APIRouter(
    prefix="/certifications",
    tags=["certifications"],
)

certifications_db: List[Certification] = []

@router.get("/", response_model=List[Certification])
def list_certifications():
    return certifications_db

@router.post("/", response_model=Certification)
def create_certification(cert: Certification):
    certifications_db.append(cert)
    return cert

@router.get("/{cert_id}", response_model=Certification)
def get_certification(cert_id: str):
    for cert in certifications_db:
        if cert.id == cert_id:
            return cert
    raise HTTPException(status_code=404, detail="Certification not found")

@router.put("/{cert_id}", response_model=Certification)
def update_certification(cert_id: str, cert_update: Certification):
    for i, cert in enumerate(certifications_db):
        if cert.id == cert_id:
            certifications_db[i] = cert_update
            return cert_update
    raise HTTPException(status_code=404, detail="Certification not found")

@router.delete("/{cert_id}")
def delete_certification(cert_id: str):
    for i, cert in enumerate(certifications_db):
        if cert.id == cert_id:
            del certifications_db[i]
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Certification not found")
