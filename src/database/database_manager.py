import sqlite3
import logging
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.current_time = "2025-02-07 14:20:30"
        self.db_path = "data/skill_matrix.db"
        self.init_db()

    def init_db(self):
        """データベースの初期化"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # テーブルの作成
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    group_id INTEGER,
                    FOREIGN KEY (group_id) REFERENCES groups (id)
                )
            """)

            # テストデータの挿入
            cursor.execute("SELECT COUNT(*) FROM groups")
            if cursor.fetchone()[0] == 0:
                cursor.executemany(
                    "INSERT INTO groups (name) VALUES (?)",
                    [("開発チーム1",), ("開発チーム2",), ("マネジメントチーム",)]
                )
                self.logger.info("テストデータの挿入が完了しました")

            conn.commit()
            self.logger.info("データベースの初期化が完了しました")

        except Exception as e:
            self.logger.error(f"データベースの初期化エラー: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()

    def get_all_groups(self):
        """全グループの取得"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM groups")
            return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"グループ取得エラー: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()

    def get_users_by_group(self, group_id):
        """グループに属するユーザーの取得"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name FROM users WHERE group_id = ?",
                (group_id,)
            )
            return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"ユーザー取得エラー: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
