from typing import List, Optional
from pydantic import BaseModel

class RgpdActionDetail(BaseModel):
    action_id: int
    label: str
    answer: str
    critical: bool
    advice: Optional[str]
    comment: Optional[str]

class ScoreResponse(BaseModel):
    score: int
    total: int
    conforme: int
    non_conforme: int
    critical_ko: List[RgpdActionDetail]
    ko: List[RgpdActionDetail]
    details: List[RgpdActionDetail]
