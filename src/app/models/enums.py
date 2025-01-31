# src/app/models/enums.py
from enum import Enum, auto

class ProficiencyLevel(str, Enum):
    """スキル熟練度レベルの列挙型"""
    BEGINNER = "BEGINNER"        # 初心者
    INTERMEDIATE = "INTERMEDIATE" # 中級者
    ADVANCED = "ADVANCED"        # 上級者
    EXPERT = "EXPERT"            # エキスパート

class UserRole(str, Enum):
    """ユーザーロールの列挙型"""
    ADMIN = "ADMIN"      # 管理者
    USER = "USER"        # 一般ユーザー