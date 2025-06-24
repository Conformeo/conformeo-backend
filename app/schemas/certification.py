from pydantic import BaseModel

class Certification(BaseModel):
    id: str
    name: str
    validUntil: str
    status: str  # Ou Literal['OK', 'DUE', 'TO_SCHEDULE'] si tu veux
