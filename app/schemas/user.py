from typing import Annotated
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]

class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    email: Annotated[EmailStr, Field(default=None)]
    password: Annotated[str, Field(default=None, min_length=8)]
    model_config = ConfigDict(from_attributes=True)
