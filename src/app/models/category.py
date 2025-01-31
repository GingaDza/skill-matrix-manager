# src/app/models/category.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from .base import TimestampMixin

class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # リレーションシップ
    parent = relationship("Category", remote_side=[id], backref="children")
    skills = relationship("Skill", back_populates="category")

    def __repr__(self):
        return f"<Category(name='{self.name}')>"