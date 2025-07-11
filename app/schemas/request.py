from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RgpdRequestBase(BaseModel):
    user_id: int
    type: str
    message: Optional[str] = None

class RgpdRequestCreate(RgpdRequestBase):
    pass

class RgpdRequestUpdate(BaseModel):
    status: Optional[str] = None
    note: Optional[str] = None
    date_closed: Optional[datetime] = None

class RgpdRequestRead(RgpdRequestBase):
    id: int
    status: str
    date_submitted: datetime
    date_closed: Optional[datetime] = None
    note: Optional[str] = None

    class Config:
        from_attributes = True  # Pydantic v2
