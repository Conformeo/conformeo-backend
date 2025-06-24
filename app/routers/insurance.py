# app/routers/insurances.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.insurance import Insurance

router = APIRouter(
    prefix="/insurances",
    tags=["insurances"],
)

insurances_db: List[Insurance] = []

@router.get("/", response_model=List[Insurance])
def list_insurances():
    return insurances_db

@router.post("/", response_model=Insurance)
def create_insurance(ins: Insurance):
    insurances_db.append(ins)
    return ins

@router.get("/{ins_id}", response_model=Insurance)
def get_insurance(ins_id: str):
    for ins in insurances_db:
        if ins.id == ins_id:
            return ins
    raise HTTPException(status_code=404, detail="Insurance not found")

@router.put("/{ins_id}", response_model=Insurance)
def update_insurance(ins_id: str, ins_update: Insurance):
    for i, ins in enumerate(insurances_db):
        if ins.id == ins_id:
            insurances_db[i] = ins_update
            return ins_update
    raise HTTPException(status_code=404, detail="Insurance not found")

@router.delete("/{ins_id}")
def delete_insurance(ins_id: str):
    for i, ins in enumerate(insurances_db):
        if ins.id == ins_id:
            del insurances_db[i]
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Insurance not found")
