"""データベース管理クラス"""
import sqlite3
import logging
from typing import List, Optional, Dict, Any
from .base_manager import BaseManager
from .managers.group_manager import GroupManager
from .managers.category_manager import CategoryManager
from .managers.skill_manager import SkillManager

class DatabaseManager(GroupManager, CategoryManager, SkillManager):
    """データベース管理クラス"""
    
    def __init__(self, db_path: str = "skill_matrix.db"):
        """初期化"""
        super().__init__(db_path)
        self.init_db()
    
    def init_db(self):
        """データベースを初期化"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                
                # テーブル作成
                self._create_tables(cursor)
                
                conn.commit()
                self.logger.info(f"データベースの初期化が完了しました: {self._db_path}")
        except Exception as e:
            self.logger.exception("データベースの初期化に失敗しました")
            raise

    def _create_tables(self, cursor):
        """テーブルを作成"""
        # グループテーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # ... 他のテーブル作成
