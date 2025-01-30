from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Skill(Base, TimestampMixin):
    __tablename__ = 'skills'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    
    category = relationship("Category", back_populates="skills")
    # 評価へのリレーションシップを追加
    assessments = relationship("SkillAssessment", back_populates="skill")

    def __repr__(self):
        return f"<Skill(name='{self.name}')>"