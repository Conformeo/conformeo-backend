from pydantic import BaseModel
from typing import Optional

class Site(BaseModel):
    id: str
    name: str
    address: str
    zipCode: str
    city: str
    score: Optional[float] = None
