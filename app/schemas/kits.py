from pydantic import BaseModel

class Kits(BaseModel):
    id: str
    site: str
    expiry: str
    state: str  # Ou Literal['OK', 'DUE', 'TO_SCHEDULE'] si tu veux
