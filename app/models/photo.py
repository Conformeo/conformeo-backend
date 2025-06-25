from pydantic import BaseModel

class SitePhoto(BaseModel):
    fileUrl: str
    uploadedAt: str
