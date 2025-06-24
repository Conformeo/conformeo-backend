from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel, Field

from app.schemas.extinguishers import FireExtinguisher

router = APIRouter(
    prefix="/extinguishers",
    tags=["extinguishers"],
)

# Stockage en mémoire
extinguishers_db: List[FireExtinguisher] = []

@router.get("/", response_model=List[FireExtinguisher])
def list_extinguishers():
    return extinguishers_db

@router.post("/", response_model=FireExtinguisher)
def create_extinguisher(ext: FireExtinguisher):
    extinguishers_db.append(ext)
    return ext

@router.get("/{ext_id}", response_model=FireExtinguisher)
def get_extinguisher(ext_id: str):
    for ext in extinguishers_db:
        if ext.id == ext_id:
            return ext
    raise HTTPException(status_code=404, detail="Extinguisher not found")

@router.put("/{ext_id}", response_model=FireExtinguisher)
def update_extinguisher(ext_id: str, ext_update: FireExtinguisher):
    for i, ext in enumerate(extinguishers_db):
        if ext.id == ext_id:
            extinguishers_db[i] = ext_update
            return ext_update
    raise HTTPException(status_code=404, detail="Extinguisher not found")

@router.delete("/{ext_id}")
def delete_extinguisher(ext_id: str):
    for i, ext in enumerate(extinguishers_db):
        if ext.id == ext_id:
            del extinguishers_db[i]
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Extinguisher not found")