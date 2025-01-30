# src/app/models/category.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from .base import Base, TimestampMixin

class Category(Base, TimestampMixin):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    
    # スキルとのリレーションシップ
    skills = relationship("Skill", back_populates="category")
    
    # 自己参照リレーションシップ
    parent = relationship(
        "Category",
        backref=backref('children', cascade='all, delete-orphan'),
        remote_side=[id]
    )

    def __repr__(self):
        return f"<Category(name='{self.name}')>"