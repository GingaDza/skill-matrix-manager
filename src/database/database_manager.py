"""データベースマネージャークラス"""
import os
import sqlite3
import logging
from typing import Optional, Tuple, List
from .interfaces import IDataManager
from .exceptions import DatabaseError, EntityNotFoundError

class DatabaseManager(IDataManager):
    """データベース操作を管理するクラス"""
    
    def __init__(self, db_path: str = "skill_matrix.db"):
        """初期化"""
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.current_time = "2025-02-08 03:29:29"
        
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()
        self.logger.info("データベースの初期化が完了しました")

    def _init_db(self):
        """データベースを初期化する"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            
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

    def add_group(self, name: str) -> bool:
        """グループを追加"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO groups (name, created_at, updated_at) VALUES (?, ?, ?)",
                    (name, self.current_time, self.current_time)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            self.logger.exception("グループ追加エラー")
            raise DatabaseError("データベース操作エラー") from e

    def get_group_id_by_name(self, name: str) -> Optional[int]:
        """グループ名からIDを取得"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM groups WHERE name = ?", (name,))
                result = cursor.fetchone()
                if not result:
                    raise EntityNotFoundError(f"グループが見つかりません: {name}")
                return result[0]
        except EntityNotFoundError:
            raise
        except Exception as e:
            self.logger.exception("グループID取得エラー")
            raise DatabaseError("データベース操作エラー") from e

    def get_category_id_by_name(self, name: str, group_name: str) -> Optional[int]:
        """カテゴリー名からIDを取得"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id FROM categories WHERE name = ? AND group_name = ?",
                    (name, group_name)
                )
                result = cursor.fetchone()
                if not result:
                    raise EntityNotFoundError(f"カテゴリーが見つかりません: {name} (グループ: {group_name})")
                return result[0]
        except EntityNotFoundError:
            raise
        except Exception as e:
            self.logger.exception("カテゴリーID取得エラー")
            raise DatabaseError("データベース操作エラー") from e

    def get_group_by_id(self, group_id: int) -> Tuple[str, str, str]:
        """グループIDからグループ情報を取得"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT name, created_at, updated_at FROM groups WHERE id = ?",
                    (group_id,)
                )
                result = cursor.fetchone()
                if not result:
                    raise EntityNotFoundError(f"グループが見つかりません: ID={group_id}")
                return result
        except EntityNotFoundError:
            raise
        except Exception as e:
            self.logger.exception("グループ情報取得エラー")
            raise DatabaseError("データベース操作エラー") from e
