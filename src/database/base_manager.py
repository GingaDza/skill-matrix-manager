"""データベース基本操作のミックスイン"""
import os
import sqlite3
import logging
from typing import Optional

class BaseManagerMixin:
    """データベース基本操作を提供するミックスイン"""
    
    def __init__(self, db_path: str = "skill_matrix.db"):
        """
        初期化
        
        Args:
            db_path (str): データベースファイルのパス
        """
        self.logger = logging.getLogger(__name__)
        self._db_path = db_path
        self.current_time = "2025-02-08 02:37:08"
        
        # 古いDBファイルが存在する場合は削除
        if os.path.exists(self._db_path):
            os.remove(self._db_path)
            self.logger.info("古いデータベースファイルを削除しました")
            
        # テーブルを作成
        self._create_tables()
        self.logger.info("データベースの初期化が完了しました")

    def _get_connection(self) -> sqlite3.Connection:
        """
        データベース接続を取得する
        
        Returns:
            sqlite3.Connection: データベース接続
        """
        return sqlite3.connect(self._db_path)

    def _create_tables(self):
        """テーブルを作成する"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # グループテーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS groups (
                    group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            # カテゴリーテーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    group_id INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (group_id) REFERENCES groups (group_id),
                    UNIQUE (name, group_id)
                )
            """)
            
            # スキルテーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    parent_id INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (parent_id) REFERENCES categories (category_id),
                    UNIQUE (name, parent_id)
                )
            """)
            
            # 評価テーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS evaluations (
                    evaluation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_id INTEGER NOT NULL,
                    level INTEGER NOT NULL CHECK (level BETWEEN 0 AND 5),
                    memo TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (skill_id) REFERENCES skills (skill_id)
                )
            """)
            
            conn.commit()
