# src/desktop/models/entities/skill.py
"""
Skill model
Created: 2025-01-31 22:50:28
Author: GingaDza
"""
from .base import BaseModel

class Skill(BaseModel):
    def __init__(self, id: str, name: str, category_id: str, description: str = ""):
        super().__init__(id, name, description)
        self.category_id = category_id