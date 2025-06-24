# app/routers/kits.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.kits import Kits

router = APIRouter(
    prefix="/kits",
    tags=["kits"],
)

kits_db: List[Kits] = []

@router.get("/", response_model=List[Kits])
def list_kits():
    return kits_db

@router.post("/", response_model=Kits)
def create_kit(kit: Kits):
    kits_db.append(kit)
    return kit

@router.get("/{kit_id}", response_model=Kits)
def get_kit(kit_id: str):
    for kit in kits_db:
        if kit.id == kit_id:
            return kit
    raise HTTPException(status_code=404, detail="Kit not found")

@router.put("/{kit_id}", response_model=Kits)
def update_kit(kit_id: str, kit_update: Kits):
    for i, kit in enumerate(kits_db):
        if kit.id == kit_id:
            kits_db[i] = kit_update
            return kit_update
    raise HTTPException(status_code=404, detail="Kit not found")

@router.delete("/{kit_id}")
def delete_kit(kit_id: str):
    for i, kit in enumerate(kits_db):
        if kit.id == kit_id:
            del kits_db[i]
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Kit not found")
