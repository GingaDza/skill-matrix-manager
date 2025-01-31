# src/app/schemas/skill_assessment.py
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from .base import TimestampSchema
from ..models.enums import ProficiencyLevel

# 循環インポートを削除
# from ..schemas.skill_assessment import (  # この行を削除

class SkillAssessmentBase(BaseModel):
    skill_id: int
    proficiency_level: ProficiencyLevel

class SkillAssessmentCreate(SkillAssessmentBase):
    pass

class SkillAssessment(SkillAssessmentBase, TimestampSchema):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class SkillAssessmentResponse(SkillAssessment):
    skill_name: str | None = None
    user_name: str | None = None

class SkillAssessmentUpdate(BaseModel):
    proficiency_level: ProficiencyLevel

class UserSkillAssessment(BaseModel):
    skill_id: int
    skill_name: str
    proficiency_level: ProficiencyLevel
    assessed_at: datetime