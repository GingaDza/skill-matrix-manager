# src/app/schemas/skill.py
from typing import Optional
from pydantic import BaseModel
from .base import TimestampSchema

class SkillBase(BaseModel):
    name: str
    description: str | None = None
    category_id: int | None = None

class SkillCreate(SkillBase):
    pass

# これがインポートエラーの原因。SkillModelからSkillに名前を変更
class Skill(SkillBase, TimestampSchema):
    id: int

    class Config:
        from_attributes = True

class SkillUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category_id: int | None = None

class SkillResponse(Skill):
    category_name: str | None = None