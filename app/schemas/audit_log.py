from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class AuditLogBase(BaseModel):
    user_id: int
    action: str
    object_type: str
    object_id: int
    details: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogRead(AuditLogBase):
    id: int
    created_at: datetime  # ⬅️ Plus standard, tu peux garder 'timestamp' si tu veux

    model_config = ConfigDict(from_attributes=True)  # Pydantic v2
    # Si tu restes sur Pydantic v1 : décommente la ligne ci-dessous
    # class Config:
    #     orm_mode = True

# Si tu préfères vraiment "timestamp", change created_at en timestamp PARTOUT (ORM + API)
