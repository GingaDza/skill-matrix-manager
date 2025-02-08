"""データベース管理モジュール"""
import sqlite3
import logging
from pathlib import Path
from typing import List, Optional

class DatabaseManager:
    """データベース管理クラス"""
    
    def __init__(self, db_path: str = "skill_matrix.db"):
        """
        初期化
        
        Args:
            db_path: データベースファイルのパス
        """
        self.logger = logging.getLogger(__name__)
        self._db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """データベースを初期化"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                
                # グループテーブル
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS groups (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # ユーザーテーブル
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        group_id INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (group_id) REFERENCES groups(id)
                    )
                """)
                
                # カテゴリーテーブル
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS categories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        parent_id INTEGER,
                        group_id INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (parent_id) REFERENCES categories(id),
                        FOREIGN KEY (group_id) REFERENCES groups(id)
                    )
                """)
                
                # スキルテーブル
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS skills (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category_id INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (category_id) REFERENCES categories(id)
                    )
                """)
                
                # スキルレベルテーブル
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS skill_levels (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        skill_id INTEGER,
                        level INTEGER NOT NULL DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id),
                        FOREIGN KEY (skill_id) REFERENCES skills(id)
                    )
                """)
                
                conn.commit()
                self.logger.info(f"データベースの初期化が完了しました: {self._db_path}")
        except Exception as e:
            self.logger.exception("データベースの初期化に失敗しました")
            raise

    def get_groups(self) -> List[str]:
        """
        グループ一覧を取得
        
        Returns:
            List[str]: グループ名のリスト
        """
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM groups ORDER BY name")
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            self.logger.exception("グループの取得に失敗しました")
            raise

    def add_group(self, name: str) -> None:
        """
        グループを追加
        
        Args:
            name: グループ名
        """
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO groups (name) VALUES (?)",
                    (name,)
                )
                conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"グループ名 '{name}' は既に存在します")
        except Exception as e:
            self.logger.exception("グループの追加に失敗しました")
            raise

    def update_group(self, old_name: str, new_name: str) -> None:
        """
        グループ名を更新
        
        Args:
            old_name: 現在のグループ名
            new_name: 新しいグループ名
        """
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE groups SET name = ?, updated_at = CURRENT_TIMESTAMP WHERE name = ?",
                    (new_name, old_name)
                )
                if cursor.rowcount == 0:
                    raise ValueError(f"グループ '{old_name}' が見つかりません")
                conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"グループ名 '{new_name}' は既に存在します")
        except Exception as e:
            self.logger.exception("グループの更新に失敗しました")
            raise

    def delete_group(self, name: str) -> None:
        """
        グループを削除
        
        Args:
            name: グループ名
        """
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                # 関連するデータを削除
                cursor.execute(
                    """
                    DELETE FROM skill_levels 
                    WHERE user_id IN (
                        SELECT id FROM users WHERE group_id = (
                            SELECT id FROM groups WHERE name = ?
                        )
                    )
                    """,
                    (name,)
                )
                cursor.execute(
                    """
                    DELETE FROM users 
                    WHERE group_id = (
                        SELECT id FROM groups WHERE name = ?
                    )
                    """,
                    (name,)
                )
                cursor.execute(
                    "DELETE FROM groups WHERE name = ?",
                    (name,)
                )
                if cursor.rowcount == 0:
                    raise ValueError(f"グループ '{name}' が見つかりません")
                conn.commit()
        except Exception as e:
            self.logger.exception("グループの削除に失敗しました")
            raise

    def get_users(self, group_name: str) -> List[str]:
        """
        グループに属するユーザー一覧を取得
        
        Args:
            group_name: グループ名
            
        Returns:
            List[str]: ユーザー名のリスト
        """
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT users.name 
                    FROM users 
                    JOIN groups ON users.group_id = groups.id 
                    WHERE groups.name = ?
                    ORDER BY users.name
                    """,
                    (group_name,)
                )
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            self.logger.exception("ユーザーの取得に失敗しました")
            raise

    def add_user(self, name: str, group_name: str) -> None:
        """
        ユーザーを追加
        
        Args:
            name: ユーザー名
            group_name: グループ名
        """
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO users (name, group_id)
                    VALUES (?, (SELECT id FROM groups WHERE name = ?))
                    """,
                    (name, group_name)
                )
                conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"ユーザー名 '{name}' は既に存在します")
        except Exception as e:
            self.logger.exception("ユーザーの追加に失敗しました")
            raise

    def update_user(self, old_name: str, new_name: str, group_name: str) -> None:
        """
        ユーザー名を更新
        
        Args:
            old_name: 現在のユーザー名
            new_name: 新しいユーザー名
            group_name: グループ名
        """
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE users 
                    SET name = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE name = ? AND group_id = (
                        SELECT id FROM groups WHERE name = ?
                    )
                    """,
                    (new_name, old_name, group_name)
                )
                if cursor.rowcount == 0:
                    raise ValueError(f"ユーザー '{old_name}' が見つかりません")
                conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"ユーザー名 '{new_name}' は既に存在します")
        except Exception as e:
            self.logger.exception("ユーザーの更新に失敗しました")
            raise

    def delete_user(self, name: str, group_name: str) -> None:
        """
        ユーザーを削除
        
        Args:
            name: ユーザー名
            group_name: グループ名
        """
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                # スキルレベルを削除
                cursor.execute(
                    """
                    DELETE FROM skill_levels 
                    WHERE user_id = (
                        SELECT id FROM users 
                        WHERE name = ? AND group_id = (
                            SELECT id FROM groups WHERE name = ?
                        )
                    )
                    """,
                    (name, group_name)
                )
                # ユーザーを削除
                cursor.execute(
                    """
                    DELETE FROM users 
                    WHERE name = ? AND group_id = (
                        SELECT id FROM groups WHERE name = ?
                    )
                    """,
                    (name, group_name)
                )
                if cursor.rowcount == 0:
                    raise ValueError(f"ユーザー '{name}' が見つかりません")
                conn.commit()
        except Exception as e:
            self.logger.exception("ユーザーの削除に失敗しました")
            raise
