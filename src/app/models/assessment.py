# src/app/models/assessment.py
from sqlalchemy import Column, Integer, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from .base import Base, TimestampMixin

class ProficiencyLevel(enum.Enum):
    NOVICE = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4

class SkillAssessment(Base, TimestampMixin):
    __tablename__ = 'skill_assessments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skills.id'), nullable=False)
    proficiency_level = Column(Integer, nullable=False)
    notes = Column(Text)
    
    user = relationship("User", back_populates="skill_assessments")
    skill = relationship("Skill", back_populates="assessments")

    def __repr__(self):
        return f"<SkillAssessment(user_id={self.user_id}, skill_id={self.skill_id}, level={self.proficiency_level})>"