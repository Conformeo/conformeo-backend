# app/schemas/site.py
from pydantic import BaseModel
from typing import Optional, List

class SiteBase(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    zipCode: Optional[str] = None
    score: Optional[int] = None

class SiteCreate(SiteBase):
    pass

class SiteRead(SiteBase):
    id: int

class SitePhoto(BaseModel):
    filename: str
    fileUrl: str
    uploadedAt: str

class SiteDocument(BaseModel):
    filename: str
    fileUrl: str
    uploadedAt: str

class SiteRead(BaseModel):
    id: str
    name: str
    address: str
    city: str
    zipCode: str
    score: int

    class Config:
        from_attributes = True  # si Pydantic v2

class SitePhotoRead(BaseModel):
    filename: str
    fileUrl: str
    uploadedAt: str

class SiteDocumentRead(BaseModel):
    filename: str
    fileUrl: str
    uploadedAt: str
