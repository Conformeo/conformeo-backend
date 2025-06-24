# app/routers/cameras.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.camera import Camera

router = APIRouter(
    prefix="/cameras",
    tags=["cameras"],
)

cameras_db: List[Camera] = []

@router.get("/", response_model=List[Camera])
def list_cameras():
    return cameras_db

@router.post("/", response_model=Camera)
def create_camera(cam: Camera):
    cameras_db.append(cam)
    return cam

@router.get("/{cam_id}", response_model=Camera)
def get_camera(cam_id: str):
    for cam in cameras_db:
        if cam.id == cam_id:
            return cam
    raise HTTPException(status_code=404, detail="Camera not found")

@router.put("/{cam_id}", response_model=Camera)
def update_camera(cam_id: str, cam_update: Camera):
    for i, cam in enumerate(cameras_db):
        if cam.id == cam_id:
            cameras_db[i] = cam_update
            return cam_update
    raise HTTPException(status_code=404, detail="Camera not found")

@router.delete("/{cam_id}")
def delete_camera(cam_id: str):
    for i, cam in enumerate(cameras_db):
        if cam.id == cam_id:
            del cameras_db[i]
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Camera not found")
