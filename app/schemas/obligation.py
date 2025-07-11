from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class ObligationBase(BaseModel):
    label: str
    status: bool = False
    last_update: Optional[date] = None
    user_id: int

class ObligationCreate(ObligationBase):
    pass

class ObligationUpdate(BaseModel):
    status: Optional[bool] = None
    last_update: Optional[date] = None

class ObligationRead(ObligationBase):
    id: int
    model_config = ConfigDict(from_attributes=True)  # Pour Pydantic v2+
