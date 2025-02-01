# src/desktop/models/data_manager/skill.py
"""
Skill and category management implementation
Created: 2025-01-31 22:32:29
Author: GingaDza
"""
from PySide6.QtCore import Signal
from uuid import uuid4
from .base import BaseManager
from ..entities import Category, Skill

class SkillManager(BaseManager):
    categories_changed = Signal()
    skills_changed = Signal()
    
    def __init__(self):
        super().__init__()
        self.categories = {}
        self.skills = {}
    
    def create_category(self, name: str, description: str = "") -> str:
        """新規カテゴリーの作成"""
        if not name:
            raise ValueError("カテゴリー名は必須です")
        
        for category in self.categories.values():
            if category.name == name:
                raise ValueError(f"カテゴリー名 {name} は既に使用されています")
        
        category_id = str(uuid4())
        category = Category(id=category_id, name=name, description=description)
        self.categories[category_id] = category
        
        self._update_modified()
        self.categories_changed.emit()
        
        return category_id
    
    def create_skill(self, name: str, category_id: str, description: str = "") -> str:
        """新規スキルの作成"""
        if not name:
            raise ValueError("スキル名は必須です")
        
        if not category_id or category_id not in self.categories:
            raise ValueError("有効なカテゴリーを指定してください")
        
        for skill in self.skills.values():
            if skill.category_id == category_id and skill.name == name:
                raise ValueError(f"スキル名 {name} は既に使用されています")
        
        skill_id = str(uuid4())
        skill = Skill(id=skill_id, name=name, category_id=category_id, description=description)
        self.skills[skill_id] = skill
        self.categories[category_id].add_skill(skill_id)
        
        self._update_modified()
        self.skills_changed.emit()
        
        return skill_id
    
    def get_group_categories(self, group_id: str = None) -> list:
        """カテゴリー一覧を取得"""
        return sorted(self.categories.values(), key=lambda x: x.name)
    
    def get_category_skills(self, category_id: str) -> list:
        """カテゴリーのスキル一覧を取得"""
        if not category_id:
            return []
        return sorted(
            [s for s in self.skills.values() if s.category_id == category_id],
            key=lambda x: x.name
        )