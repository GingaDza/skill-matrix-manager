# src/desktop/models/user.py
"""
User model implementation
Created: 2025-01-31 13:52:25
Author: GingaDza
"""
from .base import BaseModel

class User(BaseModel):
    def __init__(self, id: str, name: str, email: str, group_id: str = None):
        super().__init__(id)
        self.name = name
        self.email = email
        self.group_id = group_id
        self.skill_levels = {}  # スキルレベルを保存するディクショナリ
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("名前は必須です")
        self._name = value.strip()
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str):
        if not value or '@' not in value:
            raise ValueError("有効なメールアドレスを指定してください")
        self._email = value.strip().lower()