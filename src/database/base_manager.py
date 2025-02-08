"""データベースの基本操作を管理するモジュール"""
import sqlite3
import os
import logging
from typing import List, Optional, Tuple

class BaseManagerMixin:
    """データベースの基本操作を提供するミックスイン"""

    def __init__(self, db_path: str = "skill_matrix.db"):
        """
        初期化
        
        Args:
            db_path (str): データベースファイルのパス
        """
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.current_time = "2025-02-08 03:12:16"
        
        # 古いデータベースを削除
        if os.path.exists(db_path):
            os.remove(db_path)
            self.logger.info("古いデータベースファイルを削除しました")
            
        # データベースを初期化
        self._init_db()
        self.logger.info("データベースの初期化が完了しました")

    def _init_db(self):
        """データベースを初期化する"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # グループテーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            # カテゴリーテーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    group_name TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(name, group_name),
                    FOREIGN KEY (group_name) REFERENCES groups(name)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
                )
            """)
            
            # スキルテーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category_name TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(name, category_name),
                    FOREIGN KEY (category_name) REFERENCES categories(name)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
                )
            """)
            
            conn.commit()

    def get_groups(self) -> List[str]:
        """
        全てのグループ名を取得
        
        Returns:
            List[str]: グループ名のリスト
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM groups ORDER BY name")
            return [row[0] for row in cursor.fetchall()]

    def add_group(self, name: str) -> bool:
        """
        グループを追加
        
        Args:
            name (str): グループ名
            
        Returns:
            bool: 成功したらTrue
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO groups (name, created_at, updated_at) VALUES (?, ?, ?)",
                    (name, self.current_time, self.current_time)
                )
                return True
        except sqlite3.IntegrityError:
            return False

    def rename_group(self, old_name: str, new_name: str) -> bool:
        """
        グループ名を変更
        
        Args:
            old_name (str): 現在のグループ名
            new_name (str): 新しいグループ名
            
        Returns:
            bool: 成功したらTrue
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE groups SET name = ?, updated_at = ? WHERE name = ?",
                    (new_name, self.current_time, old_name)
                )
                return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False

    def delete_group(self, name: str) -> bool:
        """
        グループを削除
        
        Args:
            name (str): グループ名
            
        Returns:
            bool: 成功したらTrue
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM groups WHERE name = ?", (name,))
            return cursor.rowcount > 0

    def get_categories_by_group(self, group_name: str) -> List[str]:
        """
        指定したグループのカテゴリー一覧を取得
        
        Args:
            group_name (str): グループ名
            
        Returns:
            List[str]: カテゴリー名のリスト
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM categories WHERE group_name = ? ORDER BY name",
                (group_name,)
            )
            return [row[0] for row in cursor.fetchall()]

    def add_category(self, name: str, group_name: str) -> bool:
        """
        カテゴリーを追加
        
        Args:
            name (str): カテゴリー名
            group_name (str): グループ名
            
        Returns:
            bool: 成功したらTrue
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO categories (name, group_name, created_at, updated_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (name, group_name, self.current_time, self.current_time)
                )
                return True
        except sqlite3.IntegrityError:
            return False

    def rename_category(self, old_name: str, new_name: str, group_name: str) -> bool:
        """
        カテゴリー名を変更
        
        Args:
            old_name (str): 現在のカテゴリー名
            new_name (str): 新しいカテゴリー名
            group_name (str): グループ名
            
        Returns:
            bool: 成功したらTrue
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE categories 
                    SET name = ?, updated_at = ? 
                    WHERE name = ? AND group_name = ?
                    """,
                    (new_name, self.current_time, old_name, group_name)
                )
                return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False

    def delete_category(self, name: str, group_name: str) -> bool:
        """
        カテゴリーを削除
        
        Args:
            name (str): カテゴリー名
            group_name (str): グループ名
            
        Returns:
            bool: 成功したらTrue
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM categories WHERE name = ? AND group_name = ?",
                (name, group_name)
            )
            return cursor.rowcount > 0

    def get_skills_by_parent(self, category_name: str) -> List[str]:
        """
        指定したカテゴリーのスキル一覧を取得
        
        Args:
            category_name (str): カテゴリー名
            
        Returns:
            List[str]: スキル名のリスト
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM skills WHERE category_name = ? ORDER BY name",
                (category_name,)
            )
            return [row[0] for row in cursor.fetchall()]

    def add_skill(self, name: str, category_name: str) -> bool:
        """
        スキルを追加
        
        Args:
            name (str): スキル名
            category_name (str): カテゴリー名
            
        Returns:
            bool: 成功したらTrue
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO skills (name, category_name, created_at, updated_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (name, category_name, self.current_time, self.current_time)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            self.logger.exception("スキル追加エラー")
            return False

    def rename_skill(self, old_name: str, new_name: str, category_name: str) -> bool:
        """
        スキル名を変更
        
        Args:
            old_name (str): 現在のスキル名
            new_name (str): 新しいスキル名
            category_name (str): カテゴリー名
            
        Returns:
            bool: 成功したらTrue
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE skills 
                    SET name = ?, updated_at = ? 
                    WHERE name = ? AND category_name = ?
                    """,
                    (new_name, self.current_time, old_name, category_name)
                )
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False

    def delete_skill(self, name: str, category_name: str) -> bool:
        """
        スキルを削除
        
        Args:
            name (str): スキル名
            category_name (str): カテゴリー名
            
        Returns:
            bool: 成功したらTrue
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM skills WHERE name = ? AND category_name = ?",
                (name, category_name)
            )
            conn.commit()
            return cursor.rowcount > 0