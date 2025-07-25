from pydantic import ConfigDict
# app/schemas/duerp.py
from pydantic import BaseModel
from typing import Optional

class DuerpEvaluationBase(BaseModel):
    company_id: int
    title: str
    description: Optional[str]
    statut: Optional[str] = "EN_COURS"
    model_config = ConfigDict(from_attributes=True)

class DuerpEvaluationCreate(DuerpEvaluationBase):
    pass

class DuerpEvaluationRead(DuerpEvaluationBase):
    id: int
    created_at: Optional[str]

    class Config:
        orm_mode = True
