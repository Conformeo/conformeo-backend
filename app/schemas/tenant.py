# app/schemas/tenant.py

from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)


class Tenant(TenantInDBBase):
    pass
