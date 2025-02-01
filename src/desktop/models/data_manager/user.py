# src/desktop/models/data_manager/user.py
"""
User management implementation
Created: 2025-01-31 22:32:29
Author: GingaDza
"""
from PySide6.QtCore import Signal
from uuid import uuid4
from .base import BaseManager
from ..entities import User

class UserManager(BaseManager):
    users_changed = Signal()
    
    def __init__(self):
        super().__init__()
        self.users = {}
        self._current_user_id = None
    
    @property
    def current_user_id(self) -> str:
        return self._current_user_id
    
    @current_user_id.setter
    def current_user_id(self, value: str):
        if value and value not in self.users:
            raise ValueError("指定されたユーザーが存在しません")
        self._current_user_id = value
    
    def create_user(self, name: str, email: str, group_id: str = None) -> str:
        """新規ユーザーの作成"""
        if not name or not email:
            raise ValueError("名前とメールアドレスは必須です")
        
        for user in self.users.values():
            if user.email == email:
                raise ValueError(f"メールアドレス {email} は既に使用されています")
        
        user_id = str(uuid4())
        user = User(id=user_id, name=name, email=email, group_id=group_id)
        self.users[user_id] = user
        
        self._update_modified()
        self.users_changed.emit()
        
        return user_id
    
    def get_group_users(self, group_id: str = None) -> list:
        """グループに属するユーザーの取得"""
        users = self.users.values()
        if group_id:
            users = [u for u in users if u.group_id == group_id]
        return sorted(users, key=lambda x: x.name)