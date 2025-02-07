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
        self.current_time = "2025-02-07 23:47:25"
        
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
        
        # ユーザーテーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                group_id INTEGER,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (group_id) REFERENCES groups(id)
            )
        """)
        
        # 親カテゴリーテーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS parent_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        # 子カテゴリー（スキル）テーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                parent_id INTEGER,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (parent_id) REFERENCES parent_categories(id)
            )
        """)
        
        # スキル評価テーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skill_evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                skill_id INTEGER,
                level INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (skill_id) REFERENCES skills(id)
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

    def add_user(self, name: str, group_id: int) -> bool:
        """ユーザーの追加"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (name, group_id, created_at, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                (name, group_id, self.current_time, self.current_time)
            )
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.exception(f"ユーザー追加エラー: {name}")
            return False

    def get_users_in_group(self, group_name: str) -> List[str]:
        """グループ内のユーザー一覧を取得"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT u.name
                FROM users u
                JOIN groups g ON u.group_id = g.id
                WHERE g.name = ?
                ORDER BY u.name
                """,
                (group_name,)
            )
            return [row['name'] for row in cursor.fetchall()]
        except Exception as e:
            self.logger.exception(f"ユーザー一覧取得エラー: {group_name}")
            return []

    def add_parent_category(self, name: str) -> bool:
        """親カテゴリーの追加"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO parent_categories (name, created_at, updated_at)
                VALUES (?, ?, ?)
                """,
                (name, self.current_time, self.current_time)
            )
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.exception(f"親カテゴリー追加エラー: {name}")
            return False

    def get_parent_categories(self) -> List[str]:
        """親カテゴリー一覧の取得"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM parent_categories ORDER BY name")
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

    def get_skills_by_parent(self, parent_name: str) -> List[str]:
        """親カテゴリーに属するスキル一覧の取得"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT s.name
                FROM skills s
                JOIN parent_categories p ON s.parent_id = p.id
                WHERE p.name = ?
                ORDER BY s.name
                """,
                (parent_name,)
            )
            return [row['name'] for row in cursor.fetchall()]
        except Exception as e:
            self.logger.exception(f"スキル一覧取得エラー: {parent_name}")
            return []

    def set_skill_level(self, user_id: int, skill_id: int, level: int) -> bool:
        """スキルレベルの設定"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO skill_evaluations
                (user_id, skill_id, level, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, skill_id, level, self.current_time, self.current_time)
            )
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.exception("スキルレベル設定エラー")
            return False

    def get_user_skills(self, user_name: str, category_name: str) -> Dict[str, int]:
        """ユーザーのスキルレベルを取得"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT s.name, se.level
                FROM skill_evaluations se
                JOIN users u ON se.user_id = u.id
                JOIN skills s ON se.skill_id = s.id
                JOIN parent_categories p ON s.parent_id = p.id
                WHERE u.name = ? AND p.name = ?
                """,
                (user_name, category_name)
            )
            return {row['name']: row['level'] for row in cursor.fetchall()}
        except Exception as e:
            self.logger.exception(f"スキルレベル取得エラー: {user_name}")
            return {}

    def get_group_skills(self, group_name: str) -> Dict[str, float]:
        """グループの平均スキルレベルを取得"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT s.name, AVG(se.level) as avg_level
                FROM skill_evaluations se
                JOIN users u ON se.user_id = u.id
                JOIN groups g ON u.group_id = g.id
                JOIN skills s ON se.skill_id = s.id
                WHERE g.name = ?
                GROUP BY s.name
                """,
                (group_name,)
            )
            return {row['name']: float(row['avg_level']) for row in cursor.fetchall()}
        except Exception as e:
            self.logger.exception(f"グループスキル取得エラー: {group_name}")
            return {}

    def __del__(self):
        """デストラクタ"""
        try:
            if hasattr(self, 'conn'):
                self.conn.close()
        except Exception as e:
            self.logger.exception("データベース接続終了エラー")
