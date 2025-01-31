# src/app/schemas/base.py
from pydantic import BaseModel
from datetime import datetime

class TimestampSchema(BaseModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True