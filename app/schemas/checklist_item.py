from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ChecklistItemBase(BaseModel):
    label: str
    is_done: bool = False


class ChecklistItemCreate(ChecklistItemBase):
    pass


class ChecklistItemUpdate(BaseModel):
    label: str | None = None
    is_done: bool | None = None


class ChecklistItemRead(ChecklistItemBase):
    id: int
    checklist_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
