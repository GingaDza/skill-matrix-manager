# src/app/models/skill_assessment.py
from sqlalchemy import Column, Integer, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from ..database import Base
from .base import TimestampMixin
from .enums import ProficiencyLevel

class SkillAssessment(Base, TimestampMixin):
    __tablename__ = "skill_assessments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))
    proficiency_level = Column(SQLAlchemyEnum(ProficiencyLevel))

    # リレーションシップ
    user = relationship("User", back_populates="skill_assessments")
    skill = relationship("Skill", back_populates="skill_assessments")