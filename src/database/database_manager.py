import sqlite3
import logging
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.current_time = "2025-02-07 22:01:06"
        self.db_path = "database/skill_matrix.db"
        
        # データベースディレクトリの作成
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        self.initialize_database()
        self.logger.info("データベースの初期化が完了しました")

    def get_connection(self):
        """データベース接続を取得"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except Exception as e:
            self.logger.error(f"Database connection error: {e}", exc_info=True)
            raise

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
                        deleted_at TEXT DEFAULT NULL,
                        FOREIGN KEY (group_id) REFERENCES groups (id)
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
            # グループ数を確認
            cursor.execute("SELECT COUNT(*) FROM groups")
            if cursor.fetchone()[0] == 0:
                # 初期グループの挿入
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
        """全グループの取得"""
        self.logger.debug("Fetching all groups")
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name FROM groups ORDER BY id")
                return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"Error fetching groups: {e}", exc_info=True)
            return []

    def get_users_by_group(self, group_id):
        """グループ内のユーザー取得"""
        self.logger.debug(f"Fetching users for group {group_id}")
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, name 
                    FROM users 
                    WHERE group_id = ? AND deleted_at IS NULL 
                    ORDER BY id
                    """,
                    (group_id,)
                )
                return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"Error fetching users for group {group_id}: {e}", exc_info=True)
            return []

    def add_user(self, name, group_id):
        """ユーザーの追加"""
        self.logger.debug(f"Adding user {name} to group {group_id}")
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # グループの存在確認
                cursor.execute("SELECT id FROM groups WHERE id = ?", (group_id,))
                if not cursor.fetchone():
                    self.logger.error(f"Group {group_id} does not exist")
                    return None
                
                # ユーザーの追加
                cursor.execute(
                    """
                    INSERT INTO users (name, group_id, created_at, updated_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (name, group_id, self.current_time, self.current_time)
                )
                conn.commit()
                
                new_user_id = cursor.lastrowid
                self.logger.info(f"User {name} (ID: {new_user_id}) added successfully")
                return new_user_id
                
        except sqlite3.IntegrityError as e:
            self.logger.error(f"Database integrity error adding user: {e}", exc_info=True)
            return None
        except Exception as e:
            self.logger.error(f"Error adding user: {e}", exc_info=True)
            return None

    def edit_user(self, user_id, name):
        """ユーザーの編集"""
        self.logger.debug(f"Editing user {user_id} with name {name}")
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE users 
                    SET name = ?, updated_at = ? 
                    WHERE id = ? AND deleted_at IS NULL
                    """,
                    (name, self.current_time, user_id)
                )
                conn.commit()
                
                success = cursor.rowcount > 0
                if success:
                    self.logger.info(f"User {user_id} updated successfully")
                return success
                
        except Exception as e:
            self.logger.error(f"Error editing user {user_id}: {e}", exc_info=True)
            return False

    def delete_user(self, user_id):
        """ユーザーの論理削除"""
        self.logger.debug(f"Deleting user {user_id}")
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # ユーザーの存在確認
                cursor.execute(
                    "SELECT id FROM users WHERE id = ? AND deleted_at IS NULL",
                    (user_id,)
                )
                if not cursor.fetchone():
                    self.logger.warning(f"User {user_id} not found or already deleted")
                    return False
                
                # 論理削除を実行
                cursor.execute(
                    """
                    UPDATE users 
                    SET deleted_at = ?, updated_at = ? 
                    WHERE id = ?
                    """,
                    (self.current_time, self.current_time, user_id)
                )
                conn.commit()
                
                success = cursor.rowcount > 0
                if success:
                    self.logger.info(f"User {user_id} deleted successfully")
                return success
                    
        except Exception as e:
            self.logger.error(f"Error deleting user {user_id}: {e}", exc_info=True)
            return False
