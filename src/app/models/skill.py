# src/app/models/skill.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from .base import TimestampMixin

class Skill(Base, TimestampMixin):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))

    # リレーションシップ
    category = relationship("Category", back_populates="skills")
    skill_assessments = relationship("SkillAssessment", back_populates="skill")