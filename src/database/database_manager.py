import sqlite3
import logging
from typing import List, Tuple, Optional
import os
from datetime import datetime
from contextlib import contextmanager

class DatabaseManager:
    """データベース管理クラス"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # データベースファイルの設定
        self.db_path = "data/skill_matrix.db"
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # 古いデータベースファイルを削除
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            self.logger.info("古いデータベースファイルを削除しました")
        
        # 時刻の設定
        self.current_time = "2025-02-07 22:57:05"
        
        # データベースの初期化
        self._initialize_db()
        self.logger.info("データベースの初期化が完了しました")

    @contextmanager
    def _get_connection(self):
        """データベース接続のコンテキストマネージャー"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
        except Exception as e:
            self.logger.error(f"データベース接続エラー: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    def _initialize_db(self):
        """データベースの初期化"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # 外部キー制約を有効化
                cursor.execute("PRAGMA foreign_keys = ON")
                
                # グループテーブル
                cursor.execute("""
                    CREATE TABLE groups (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                """)
                
                # ユーザーテーブル
                cursor.execute("""
                    CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        group_id INTEGER,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,
                        FOREIGN KEY (group_id) REFERENCES groups (id)
                            ON DELETE CASCADE
                    )
                """)
                
                # スキルテーブル
                cursor.execute("""
                    CREATE TABLE skills (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        category TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                """)
                
                # ユーザースキルテーブル
                cursor.execute("""
                    CREATE TABLE user_skills (
                        user_id INTEGER,
                        skill_id INTEGER,
                        level INTEGER NOT NULL DEFAULT 0,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,
                        PRIMARY KEY (user_id, skill_id),
                        FOREIGN KEY (user_id) REFERENCES users (id)
                            ON DELETE CASCADE,
                        FOREIGN KEY (skill_id) REFERENCES skills (id)
                            ON DELETE CASCADE
                    )
                """)
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"データベース初期化エラー: {e}")
            raise

    def add_group(self, name: str) -> int:
        """グループの追加"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO groups (name, created_at, updated_at)
                    VALUES (?, ?, ?)
                """, (name, self.current_time, self.current_time))
                
                conn.commit()
                return cursor.lastrowid
                
        except sqlite3.IntegrityError:
            self.logger.error(f"グループ名 '{name}' は既に存在します")
            raise ValueError(f"グループ名 '{name}' は既に使用されています")
        except Exception as e:
            self.logger.error(f"グループ追加エラー: {e}")
            raise

    def remove_group(self, group_id: int):
        """グループの削除"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    DELETE FROM groups
                    WHERE id = ?
                """, (group_id,))
                
                if cursor.rowcount == 0:
                    raise ValueError(f"グループID {group_id} が見つかりません")
                    
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"グループ削除エラー: {e}")
            raise

    def get_all_groups(self) -> List[Tuple[int, str]]:
        """全グループの取得"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, name
                    FROM groups
                    ORDER BY name
                """)
                
                return [(row[0], row[1]) for row in cursor.fetchall()]
                
        except Exception as e:
            self.logger.error(f"グループ一覧取得エラー: {e}")
            raise

    def add_user_to_group(self, name: str, group_id: int) -> int:
        """ユーザーの追加"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # グループの存在確認
                cursor.execute("""
                    SELECT id FROM groups WHERE id = ?
                """, (group_id,))
                
                if not cursor.fetchone():
                    raise ValueError(f"グループID {group_id} が見つかりません")
                
                # ユーザーの追加
                cursor.execute("""
                    INSERT INTO users (name, group_id, created_at, updated_at)
                    VALUES (?, ?, ?, ?)
                """, (name, group_id, self.current_time, self.current_time))
                
                conn.commit()
                return cursor.lastrowid
                
        except Exception as e:
            self.logger.error(f"ユーザー追加エラー: {e}")
            raise

    def remove_user(self, user_id: int):
        """ユーザーの削除"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    DELETE FROM users
                    WHERE id = ?
                """, (user_id,))
                
                if cursor.rowcount == 0:
                    raise ValueError(f"ユーザーID {user_id} が見つかりません")
                    
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"ユーザー削除エラー: {e}")
            raise

    def get_users_by_group(self, group_id: int) -> List[Tuple[int, str]]:
        """グループ内のユーザー一覧を取得"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, name
                    FROM users
                    WHERE group_id = ?
                    ORDER BY name
                """, (group_id,))
                
                return [(row[0], row[1]) for row in cursor.fetchall()]
                
        except Exception as e:
            self.logger.error(f"ユーザー一覧取得エラー: {e}")
            raise
