# app/schemas/tenant.py

from pydantic import BaseModel
from datetime import datetime


class TenantBase(BaseModel):
    name: str


class TenantCreate(TenantBase):
    pass


class TenantUpdate(TenantBase):
    pass


class TenantInDBBase(TenantBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Tenant(TenantInDBBase):
    pass
