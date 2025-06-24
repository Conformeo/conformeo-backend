from pydantic import BaseModel

class Camera(BaseModel):
    id: str
    label: str
    location: str
    lastCheck: str 
    nextCheck: str      
    zoneCovered: str
    photoUrl: str
    status: str  # Ou Literal['OK', 'DUE', 'TO_SCHEDULE'] si tu veux
