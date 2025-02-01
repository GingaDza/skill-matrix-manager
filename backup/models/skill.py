# src/desktop/models/skill.py
"""
Skill model implementation
Created: 2025-01-31 13:55:12
Author: GingaDza
"""
from .base import BaseModel

class Skill(BaseModel):
    def __init__(self, id: str, name: str, category_id: str, description: str = ""):
        super().__init__(id)
        self.name = name
        self.category_id = category_id
        self.description = description
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("スキル名は必須です")
        self._name = value.strip()
    
    @property
    def category_id(self) -> str:
        return self._category_id
    
    @category_id.setter
    def category_id(self, value: str):
        if not value:
            raise ValueError("カテゴリーIDは必須です")
        self._category_id = value
    
    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, value: str):
        self._description = value.strip() if value else ""