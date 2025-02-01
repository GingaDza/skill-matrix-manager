# src/desktop/models/category.py
"""
Category model implementation
Created: 2025-01-31 14:07:45
Author: GingaDza
"""
from .base import BaseModel

class Category(BaseModel):
    def __init__(self, id: str, name: str, description: str = ""):
        super().__init__(id)
        self.name = name
        self.description = description
        self._skills = set()  # スキルIDを保持するセット
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("カテゴリー名は必須です")
        self._name = value.strip()
    
    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, value: str):
        self._description = value.strip() if value else ""
    
    @property
    def skills(self) -> set:
        """カテゴリーに属するスキルIDのセットを返す"""
        return self._skills
    
    def add_skill(self, skill_id: str):
        """スキルの追加"""
        if skill_id:
            self._skills.add(skill_id)
    
    def remove_skill(self, skill_id: str):
        """スキルの削除"""
        self._skills.discard(skill_id)
    
    def has_skill(self, skill_id: str) -> bool:
        """スキルの存在確認"""
        return skill_id in self._skills