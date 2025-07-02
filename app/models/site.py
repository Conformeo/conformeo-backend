# app/models/site.py
from pydantic import BaseModel
from typing import Optional

class Site(BaseModel):
    id: str
    name: str
    address: str
    city: str
    zipCode: str
    score: Optional[int] = None          # ou float si besoin


class SitePhoto(BaseModel):
    filename: str
    fileUrl: str
    uploadedAt: str

class SiteDocument(BaseModel):
    filename: str
    fileUrl: str
    uploadedAt: str
