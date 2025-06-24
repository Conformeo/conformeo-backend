from pydantic import BaseModel

class FireExtinguisher(BaseModel):
    id: str
    location: str
    serialNumber: str
    lastControl: str
    nextControl: str
    status: str  # Ou Literal['OK', 'DUE', 'TO_SCHEDULE'] si tu veux