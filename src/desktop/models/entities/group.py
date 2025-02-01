# src/desktop/models/entities/group.py
"""
Group model
Created: 2025-01-31 22:50:28
Author: GingaDza
"""
from .base import BaseModel

class Group(BaseModel):
    def __init__(self, id: str, name: str, description: str = ""):
        super().__init__(id, name, description)
        self.members = set()  # ユーザーIDのセット
    
    def add_member(self, user_id: str):
        """メンバーの追加"""
        self.members.add(user_id)
        self.update_modified()
    
    def remove_member(self, user_id: str):
        """メンバーの削除"""
        if user_id in self.members:
            self.members.remove(user_id)
            self.update_modified()