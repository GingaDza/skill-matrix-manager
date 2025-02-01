# src/desktop/models/__init__.py
"""
Models package
Created: 2025-01-31 22:50:28
Author: GingaDza
"""
from .entities import User, Group, Category, Skill
from .data_manager import DataManager

__all__ = [
    'User', 'Group', 'Category', 'Skill',
    'DataManager'
]