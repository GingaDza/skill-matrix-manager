import sqlite3
import logging
from pathlib import Path
from ..logging_config import setup_logging
from datetime import datetime

class DatabaseManager:
    """データベース管理クラス"""
    
    def __init__(self, db_path='skill_matrix.db'):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        setup_logging()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def initialize_database(self):
        """データベースの初期化"""
        self.logger.info("データベースの初期化を開始")
        
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # テーブルの作成
            cursor.executescript('''
                -- グループテーブル
                CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                -- カテゴリーテーブル
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    parent_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (parent_id) REFERENCES categories(id)
                );

                -- スキルテーブル
                CREATE TABLE IF NOT EXISTS skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    category_id INTEGER,
                    max_level INTEGER DEFAULT 5,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                );

                -- スキルレベル説明テーブル
                CREATE TABLE IF NOT EXISTS skill_level_descriptions (
                    skill_id INTEGER,
                    level INTEGER,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (skill_id, level),
                    FOREIGN KEY (skill_id) REFERENCES skills(id)
                );

                -- グループ所属テーブル
                CREATE TABLE IF NOT EXISTS group_members (
                    group_id INTEGER,
                    user_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (group_id, user_id),
                    FOREIGN KEY (group_id) REFERENCES groups(id)
                );

                -- スキル評価テーブル
                CREATE TABLE IF NOT EXISTS skill_evaluations (
                    user_id INTEGER,
                    skill_id INTEGER,
                    level INTEGER,
                    evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (user_id, skill_id),
                    FOREIGN KEY (skill_id) REFERENCES skills(id)
                );
            ''')

            conn.commit()
            self.logger.info("データベースの初期化が完了しました")

        except sqlite3.Error as e:
            self.logger.error(f"データベースの初期化中にエラーが発生: {e}")
            raise
        finally:
            conn.close()

    # グループ管理メソッド
    def get_all_groups(self):
        """すべてのグループを取得"""
        query = """
        SELECT id, name, description, created_at, updated_at 
        FROM groups 
        ORDER BY name
        """
        return self.execute_query(query)

    def get_group(self, group_id):
        """指定されたIDのグループを取得"""
        query = """
        SELECT id, name, description, created_at, updated_at 
        FROM groups 
        WHERE id = ?
        """
        result = self.execute_query(query, (group_id,))
        return result[0] if result else None

    def add_group(self, name, description=""):
        """新しいグループを追加"""
        query = """
        INSERT INTO groups (name, description) 
        VALUES (?, ?)
        """
        try:
            self.execute_query(query, (name, description))
            return True
        except sqlite3.IntegrityError:
            self.logger.error(f"グループ名 '{name}' は既に存在します")
            return False

    def update_group(self, group_id, name, description=""):
        """グループ情報を更新"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = """
        UPDATE groups 
        SET name = ?, description = ?, updated_at = ? 
        WHERE id = ?
        """
        return self.execute_query(
            query, 
            (name, description, current_time, group_id)
        )

    def delete_group(self, group_id):
        """グループを削除"""
        query = "DELETE FROM groups WHERE id = ?"
        return self.execute_query(query, (group_id,))

    # データベース操作の基本メソッド
    def execute_query(self, query, params=None):
        """SQLクエリを実行"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            result = cursor.fetchall()
            conn.commit()
            return result
            
        except sqlite3.Error as e:
            self.logger.error(f"クエリ実行中にエラーが発生: {e}")
            raise
        finally:
            conn.close()

    def execute_many(self, query, params_list):
        """複数のSQLクエリを実行"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            
        except sqlite3.Error as e:
            self.logger.error(f"複数クエリ実行中にエラーが発生: {e}")
            raise
        finally:
            conn.close()
