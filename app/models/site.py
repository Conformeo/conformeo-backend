# app/models/site.py
from pydantic import BaseModel
from typing import Optional

class Site(BaseModel):
    id: str
    name: str
    address: str
    zipCode: str
    city: str
    score: Optional[int] = None

class SitePhoto(BaseModel):
    filename: str
    fileUrl: str
    uploadedAt: str

class SiteDocument(BaseModel):
    filename: str
    fileUrl: str
    uploadedAt: str
