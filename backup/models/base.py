# src/desktop/models/data_manager/base.py
"""
Base manager implementation
Created: 2025-01-31 22:32:29
Author: GingaDza
"""
from PySide6.QtCore import QObject
from datetime import datetime

class BaseManager(QObject):
    def __init__(self):
        super().__init__()
        self.created_at = datetime.utcnow()
        self.created_by = "GingaDza"
        self.last_modified_at = self.created_at
        self.last_modified_by = self.created_by
    
    def _update_modified(self):
        """最終更新情報の更新"""
        self.last_modified_at = datetime.utcnow()
        self.last_modified_by = self.created_by