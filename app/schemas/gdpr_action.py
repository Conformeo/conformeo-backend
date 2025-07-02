from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models.gdpr_action import ActionScope


class GdprActionBase(BaseModel):
    label:   str
    article: Optional[str] = None
    scope:   ActionScope   = ActionScope.ALL


class GdprActionCreate(GdprActionBase):
    pass


class GdprActionRead(BaseModel):
    id: int
    label: str
    article: str | None
    scope: ActionScope

    class Config:
        from_attributes = True
