# src/desktop/models/entities/base.py
"""
Base model implementation
Created: 2025-01-31 22:50:28
Author: GingaDza
"""
from datetime import datetime

class BaseModel:
    def __init__(self, id: str, name: str, description: str = ""):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = datetime.utcnow()
        self.created_by = "GingaDza"
        self.last_modified_at = self.created_at
        self.last_modified_by = self.created_by
    
    def update_modified(self):
        """更新情報の更新"""
        self.last_modified_at = datetime.utcnow()
        self.last_modified_by = self.created_by