"""データベース管理モジュール"""
import sqlite3
import logging
import os
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    """データベース管理クラス"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.current_time = "2025-02-08 00:33:49"
        
        try:
            self._init_database()
        except Exception as e:
            self.logger.exception("データベース初期化エラー")
            raise

    def _init_database(self):
        """データベースの初期化"""
        db_path = "data/skill_matrix.db"
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # 既存のDBファイルを削除（開発用）
        if os.path.exists(db_path):
            os.remove(db_path)
            self.logger.info("古いデータベースファイルを削除しました")
        
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        
        self._create_tables()
        self.logger.info("データベースの初期化が完了しました")

    def _create_tables(self):
        """テーブルの作成"""
        cursor = self.conn.cursor()
        
        # グループテーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        # 親カテゴリーテーブル（グループとの関連付けを追加）
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS parent_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                group_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (group_id) REFERENCES groups(id),
                UNIQUE(name, group_id)
            )
        """)
        
        # スキルテーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                parent_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (parent_id) REFERENCES parent_categories(id)
            )
        """)
        
        # ユーザーテーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                group_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (group_id) REFERENCES groups(id)
            )
        """)
        
        # スキル評価テーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skill_evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                skill_id INTEGER NOT NULL,
                level INTEGER NOT NULL CHECK (level BETWEEN 1 AND 5),
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (skill_id) REFERENCES skills(id),
                UNIQUE(user_id, skill_id)
            )
        """)
        
        self.conn.commit()

    def add_group(self, name: str) -> bool:
        """グループの追加"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO groups (name, created_at, updated_at)
                VALUES (?, ?, ?)
                """,
                (name, self.current_time, self.current_time)
            )
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.exception(f"グループ追加エラー: {name}")
            return False

    def get_groups(self) -> List[str]:
        """グループ一覧の取得"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM groups ORDER BY name")
            return [row['name'] for row in cursor.fetchall()]
        except Exception as e:
            self.logger.exception("グループ一覧取得エラー")
            return []

    def get_group_id_by_name(self, group_name: str) -> Optional[int]:
        """グループ名からIDを取得"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT id FROM groups WHERE name = ?",
                (group_name,)
            )
            result = cursor.fetchone()
            return result['id'] if result else None
        except Exception as e:
            self.logger.exception(f"グループID取得エラー: {group_name}")
            return None

    def add_parent_category(self, name: str, group_id: int) -> bool:
        """親カテゴリーの追加"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO parent_categories (name, group_id, created_at, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                (name, group_id, self.current_time, self.current_time)
            )
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.exception(f"親カテゴリー追加エラー: {name}")
            return False

    def get_parent_categories_by_group(self, group_id: int) -> List[str]:
        """グループに属する親カテゴリー一覧の取得"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT name 
                FROM parent_categories 
                WHERE group_id = ? 
                ORDER BY name
                """,
                (group_id,)
            )
            return [row['name'] for row in cursor.fetchall()]
        except Exception as e:
            self.logger.exception("親カテゴリー一覧取得エラー")
            return []

    def add_skill(self, name: str, parent_id: int) -> bool:
        """スキルの追加"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO skills (name, parent_id, created_at, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                (name, parent_id, self.current_time, self.current_time)
            )
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.exception(f"スキル追加エラー: {name}")
            return False

    def get_skills_by_parent(self, parent_id: int) -> List[str]:
        """親カテゴリーに属するスキル一覧の取得"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT name 
                FROM skills 
                WHERE parent_id = ? 
                ORDER BY name
                """,
                (parent_id,)
            )
            return [row['name'] for row in cursor.fetchall()]
        except Exception as e:
            self.logger.exception("スキル一覧取得エラー")
            return []

    def __del__(self):
        """デストラクタ"""
        try:
            if hasattr(self, 'conn'):
                self.conn.close()
        except Exception as e:
            self.logger.exception("データベース接続終了エラー")
