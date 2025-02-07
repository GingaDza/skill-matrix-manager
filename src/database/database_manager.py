import sqlite3
import logging
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.current_time = "2025-02-07 20:29:54"
        self.db_path = "database/skill_matrix.db"
        
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        self.initialize_database()
        self.logger.info("データベースの初期化が完了しました")

    def get_connection(self):
        """データベース接続を取得"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def initialize_database(self):
        """データベースの初期化"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # グループテーブル
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS groups (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                ''')
                
                # ユーザーテーブル
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        group_id INTEGER,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,
                        FOREIGN KEY (group_id) REFERENCES groups (id)
                            ON DELETE CASCADE
                    )
                ''')
                
                # 初期データの挿入
                self._insert_initial_data(cursor)
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Database initialization error: {e}", exc_info=True)
            raise

    def _insert_initial_data(self, cursor):
        """初期データの挿入"""
        try:
            cursor.execute("SELECT COUNT(*) FROM groups")
            if cursor.fetchone()[0] == 0:
                groups = [
                    ("開発部", self.current_time, self.current_time),
                    ("営業部", self.current_time, self.current_time),
                    ("管理部", self.current_time, self.current_time)
                ]
                cursor.executemany(
                    "INSERT INTO groups (name, created_at, updated_at) VALUES (?, ?, ?)",
                    groups
                )
        except Exception as e:
            self.logger.error(f"Error inserting initial data: {e}", exc_info=True)
            raise

    def get_all_groups(self):
        """全グループを取得"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name FROM groups ORDER BY id")
                return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"Error fetching groups: {e}", exc_info=True)
            return []

    def get_users_by_group(self, group_id):
        """グループに属するユーザーを取得"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, name FROM users WHERE group_id = ? ORDER BY id",
                    (group_id,)
                )
                return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"Error fetching users for group {group_id}: {e}", exc_info=True)
            return []

    def get_user(self, user_id):
        """ユーザー情報を取得"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, name, group_id FROM users WHERE id = ?",
                    (user_id,)
                )
                return cursor.fetchone()
        except Exception as e:
            self.logger.error(f"Error fetching user {user_id}: {e}", exc_info=True)
            return None

    def add_user(self, name, group_id):
        """ユーザーを追加"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO users (name, group_id, created_at, updated_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (name, group_id, self.current_time, self.current_time)
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            self.logger.error(f"Error adding user {name}: {e}", exc_info=True)
            raise

    def edit_user(self, user_id, name):
        """ユーザーを編集"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE users
                    SET name = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (name, self.current_time, user_id)
                )
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.logger.error(f"Error editing user {user_id}: {e}", exc_info=True)
            raise

    def delete_user(self, user_id):
        """ユーザーを削除"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # ユーザーの存在確認
                cursor.execute("SELECT id, name FROM users WHERE id = ?", (user_id,))
                user = cursor.fetchone()
                
                if not user:
                    self.logger.warning(f"User {user_id} not found")
                    return False
                
                # ユーザーを削除
                cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()
                
                if cursor.rowcount > 0:
                    self.logger.info(f"User {user_id} deleted successfully")
                    return True
                return False
                    
        except Exception as e:
            self.logger.error(f"Error deleting user {user_id}: {e}", exc_info=True)
            raise
