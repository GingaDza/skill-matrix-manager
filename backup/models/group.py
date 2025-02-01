# src/desktop/models/data_manager/group.py
"""
Group management implementation
Created: 2025-01-31 22:32:29
Author: GingaDza
"""
from PySide6.QtCore import Signal
from uuid import uuid4
from .base import BaseManager
from ..entities import Group

class GroupManager(BaseManager):
    groups_changed = Signal()
    
    def __init__(self):
        super().__init__()
        self.groups = {}
    
    def create_group(self, name: str, description: str = "") -> str:
        """新規グループの作成"""
        if not name:
            raise ValueError("グループ名は必須です")
        
        for group in self.groups.values():
            if group.name == name:
                raise ValueError(f"グループ名 {name} は既に使用されています")
        
        group_id = str(uuid4())
        group = Group(id=group_id, name=name, description=description)
        self.groups[group_id] = group
        
        self._update_modified()
        self.groups_changed.emit()
        
        return group_id
    
    def delete_group(self, group_id: str):
        """グループの削除"""
        if group_id not in self.groups:
            raise ValueError("指定されたグループが存在しません")
        
        del self.groups[group_id]
        self._update_modified()
        self.groups_changed.emit()
    
    def get_all_groups(self) -> list:
        """全グループ一覧を取得"""
        return sorted(self.groups.values(), key=lambda x: x.name)