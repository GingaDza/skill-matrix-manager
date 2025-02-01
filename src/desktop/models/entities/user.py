# src/desktop/models/entities/user.py
"""
User model
Created: 2025-01-31 22:50:28
Author: GingaDza
"""
from .base import BaseModel

class User(BaseModel):
    def __init__(self, id: str, name: str, email: str, group_id: str = None):
        super().__init__(id, name)
        self.email = email
        self.group_id = group_id