from pydantic import BaseModel
from typing import Optional

class RgpdExigenceBase(BaseModel):
    label: str
    article: Optional[str]
    critical: bool = False
    advice: Optional[str]

class RgpdExigenceCreate(RgpdExigenceBase):
    pass

class RgpdExigenceRead(RgpdExigenceBase):
    id: int
    class Config:
        from_attributes = True
