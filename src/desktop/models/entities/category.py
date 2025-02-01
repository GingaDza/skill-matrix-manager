# src/desktop/models/entities/category.py
"""
Category model
Created: 2025-01-31 22:50:28
Author: GingaDza
"""
from .base import BaseModel

class Category(BaseModel):
    def __init__(self, id: str, name: str, description: str = ""):
        super().__init__(id, name, description)
        self.skills = set()  # スキルIDのセット
    
    def add_skill(self, skill_id: str):
        """スキルの追加"""
        self.skills.add(skill_id)
        self.update_modified()
    
    def remove_skill(self, skill_id: str):
        """スキルの削除"""
        if skill_id in self.skills:
            self.skills.remove(skill_id)
            self.update_modified()