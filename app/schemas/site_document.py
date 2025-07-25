from pydantic import ConfigDict
# app/schemas/site_document.py

from pydantic import BaseModel
from datetime import datetime

class SiteDocumentBase(BaseModel):
    filename: str
    file_url: str
    uploaded_at: datetime
    type: str
    model_config = ConfigDict(from_attributes=True)

class SiteDocumentCreate(SiteDocumentBase):
    site_id: str

class SiteDocument(SiteDocumentBase):
    id: int
    site_id: str

    class Config:
        orm_mode = True
