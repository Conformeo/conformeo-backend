from typing import Optional
from pydantic import BaseModel

class GdprActionAnswerBase(BaseModel):
    user_id: int   # ou audit_id / tenant_id selon ton besoin
    action_id: int
    answer: str    # "Oui", "Non", "Partiellement", "Non applicable"
    comment: Optional[str] = None

class GdprActionAnswerCreate(GdprActionAnswerBase):
    pass

class GdprActionAnswerRead(GdprActionAnswerBase):
    id: int
    class Config:
        from_attributes = True
