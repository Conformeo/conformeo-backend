from typing import Optional
from pydantic import BaseModel
from app.models.gdpr_action import ActionScope

class GdprActionBase(BaseModel):
    label:   str
    article: Optional[str] = None
    scope:   ActionScope   = ActionScope.ALL
    advice:  Optional[str] = None       # <--- NOUVEAU
    critical: Optional[bool] = False    # <--- NOUVEAU

class GdprActionCreate(GdprActionBase):
    pass

class GdprActionRead(GdprActionBase):
    id: int
    class Config:
        from_attributes = True
