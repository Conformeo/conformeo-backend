from pydantic import BaseModel
from datetime import datetime

class SiteDocument(BaseModel):
    id: str
    site_id: str
    filename: str
    file_url: str
    uploaded_at: datetime
