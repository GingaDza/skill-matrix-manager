"""データベース管理モジュール"""
import sqlite3
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any

class DatabaseManager:
    """データベース管理クラス"""
    
    def __init__(self, db_path: str = "skill_matrix.db"):
        """初期化"""
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
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # カテゴリーテーブル
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS categories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        group_id INTEGER NOT NULL,
                        parent_category_id INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
                        FOREIGN KEY (parent_category_id) REFERENCES categories(id) ON DELETE CASCADE,
                        UNIQUE(name, group_id)
                    )
                """)
                
                # ユーザーテーブル
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT,
                        group_id INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
                        UNIQUE(name, group_id)
                    )
                """)
                
                # スキルテーブル
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS skills (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        category_id INTEGER NOT NULL,
                        min_level INTEGER DEFAULT 1,
                        max_level INTEGER DEFAULT 5,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
                        UNIQUE(name, category_id)
                    )
                """)
                
                # スキルレベルテーブル
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS skill_levels (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        skill_id INTEGER NOT NULL,
                        level INTEGER NOT NULL DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE,
                        UNIQUE(user_id, skill_id)
                    )
                """)
                
                conn.commit()
                self.logger.info(f"データベースの初期化が完了しました: {self._db_path}")
        except Exception as e:
            self.logger.exception("データベースの初期化に失敗しました")
            raise

    def get_groups(self) -> List[str]:
        """グループ一覧を取得"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM groups ORDER BY name")
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            self.logger.exception("グループの取得に失敗しました")
            raise

    def add_group(self, name: str, description: str = "") -> None:
        """グループを追加"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO groups (name, description) VALUES (?, ?)",
                    (name, description)
                )
                conn.commit()
                self.logger.info(f"グループを追加しました: {name}")
        except sqlite3.IntegrityError:
            raise ValueError(f"グループ名 '{name}' は既に存在します")
        except Exception as e:
            self.logger.exception("グループの追加に失敗しました")
            raise

    def get_categories(self, group_name: str) -> List[Dict[str, Any]]:
        """カテゴリー一覧を取得"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT c.name, c.description, p.name as parent_name
                    FROM categories c
                    LEFT JOIN categories p ON c.parent_category_id = p.id
                    JOIN groups g ON c.group_id = g.id
                    WHERE g.name = ?
                    ORDER BY COALESCE(p.name, c.name), c.name
                    """,
                    (group_name,)
                )
                categories = []
                for row in cursor.fetchall():
                    categories.append({
                        'name': row[0],
                        'description': row[1],
                        'parent_name': row[2]
                    })
                return categories
        except Exception as e:
            self.logger.exception("カテゴリーの取得に失敗しました")
            raise

    def add_category(self, name: str, group_name: str, parent_name: Optional[str] = None, description: str = "") -> None:
        """カテゴリーを追加"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                if parent_name:
                    cursor.execute(
                        """
                        INSERT INTO categories (name, description, group_id, parent_category_id)
                        SELECT ?, ?, g.id, p.id
                        FROM groups g
                        LEFT JOIN categories p ON p.name = ? AND p.group_id = g.id
                        WHERE g.name = ?
                        """,
                        (name, description, parent_name, group_name)
                    )
                else:
                    cursor.execute(
                        """
                        INSERT INTO categories (name, description, group_id)
                        SELECT ?, ?, id FROM groups WHERE name = ?
                        """,
                        (name, description, group_name)
                    )
                conn.commit()
                self.logger.info(f"カテゴリーを追加しました: {name} (グループ: {group_name})")
        except sqlite3.IntegrityError:
            raise ValueError(f"カテゴリー名 '{name}' は既に存在します")
        except Exception as e:
            self.logger.exception("カテゴリーの追加に失敗しました")
            raise

    def get_users(self, group_name: str) -> List[Dict[str, Any]]:
        """ユーザー一覧を取得"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT u.name, u.email
                    FROM users u
                    JOIN groups g ON u.group_id = g.id
                    WHERE g.name = ?
                    ORDER BY u.name
                    """,
                    (group_name,)
                )
                users = []
                for row in cursor.fetchall():
                    users.append({
                        'name': row[0],
                        'email': row[1]
                    })
                return users
        except Exception as e:
            self.logger.exception("ユーザーの取得に失敗しました")
            raise

    def add_user(self, name: str, group_name: str, email: Optional[str] = None) -> None:
        """ユーザーを追加"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO users (name, email, group_id)
                    SELECT ?, ?, id FROM groups WHERE name = ?
                    """,
                    (name, email, group_name)
                )
                conn.commit()
                self.logger.info(f"ユーザーを追加しました: {name} (グループ: {group_name})")
        except sqlite3.IntegrityError:
            raise ValueError(f"ユーザー名 '{name}' は既に存在します")
        except Exception as e:
            self.logger.exception("ユーザーの追加に失敗しました")
            raise
                    "min_level, max_level"
                    ") VALUES (?, ?, ?, ?, ?, ?)",
                    (name, description, category_name, group_name,
                     min_level, max_level)
                )
                conn.commit()
        except Exception as e:
            self.logger.exception("スキルの追加に失敗しました")
            raise RuntimeError(f"スキルの追加に失敗しました: {str(e)}")
    
    def update_skill(
        self,
        old_name: str,
        new_name: str,
        category_name: str,
        group_name: str,
        description: str = "",
        min_level: int = 1,
        max_level: int = 5
    ):
        """
        スキルを更新
        
        Args:
            old_name (str): 現在のスキル名
            new_name (str): 新しいスキル名
            category_name (str): カテゴリー名
            group_name (str): グループ名
            description (str, optional): 説明
            min_level (int, optional): 最小レベル
            max_level (int, optional): 最大レベル
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE skills SET "
                    "name = ?, description = ?, "
                    "min_level = ?, max_level = ?, "
                    "updated_at = CURRENT_TIMESTAMP "
                    "WHERE name = ? AND category_name = ? AND group_name = ?",
                    (new_name, description, min_level, max_level,
                     old_name, category_name, group_name)
                )
                conn.commit()
        except Exception as e:
            self.logger.exception("スキルの更新に失敗しました")
            raise RuntimeError(f"スキルの更新に失敗しました: {str(e)}")
    
    def delete_skill(self, name: str, category_name: str, group_name: str):
        """
        スキルを削除
        
        Args:
            name (str): スキル名
            category_name (str): カテゴリー名
            group_name (str): グループ名
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM skills "
                    "WHERE name = ? AND category_name = ? AND group_name = ?",
                    (name, category_name, group_name)
                )
                conn.commit()
        except Exception as e:
            self.logger.exception("スキルの削除に失敗しました")
            raise RuntimeError(f"スキルの削除に失敗しました: {str(e)}")
                    ") VALUES (?, ?, ?, ?, ?, ?)",
                    (name, description, category_name, group_name,
                     min_level, max_level)
                )
                conn.commit()
        except Exception as e:
            self.logger.exception("スキルの追加に失敗しました")
            raise RuntimeError(f"スキルの追加に失敗しました: {str(e)}")
    
    def update_skill(
        self,
        old_name: str,
        new_name: str,
        category_name: str,
        group_name: str,
        description: str = "",
        min_level: int = 1,
        max_level: int = 5
    ):
        """
        スキルを更新
        
        Args:
            old_name (str): 現在のスキル名
            new_name (str): 新しいスキル名
            category_name (str): カテゴリー名
            group_name (str): グループ名
            description (str, optional): 説明
            min_level (int, optional): 最小レベル
            max_level (int, optional): 最大レベル
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE skills SET "
                    "name = ?, description = ?, "
                    "min_level = ?, max_level = ?, "
                    "updated_at = CURRENT_TIMESTAMP "
                    "WHERE name = ? AND category_name = ? AND group_name = ?",
                    (new_name, description, min_level, max_level,
                     old_name, category_name, group_name)
                )
                conn.commit()
        except Exception as e:
            self.logger.exception("スキルの更新に失敗しました")
            raise RuntimeError(f"スキルの更新に失敗しました: {str(e)}")
    
    def delete_skill(self, name: str, category_name: str, group_name: str):
        """
        スキルを削除
        
        Args:
            name (str): スキル名
            category_name (str): カテゴリー名
            group_name (str): グループ名
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM skills "
                    "WHERE name = ? AND category_name = ? AND group_name = ?",
                    (name, category_name, group_name)
                )
                conn.commit()
        except Exception as e:
            self.logger.exception("スキルの削除に失敗しました")
            raise RuntimeError(f"スキルの削除に失敗しました: {str(e)}")
