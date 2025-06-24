from pydantic import BaseModel

class Insurance(BaseModel):
    id: str
    type: str
    provider: str
    validUntil: str
