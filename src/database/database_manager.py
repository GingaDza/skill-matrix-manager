import sqlite3
import logging
from pathlib import Path
from ..logging_config import setup_logging

class DatabaseManager:
    """データベース管理クラス"""
    
    def __init__(self, db_path='skill_matrix.db'):
        """
        Parameters:
        -----------
        db_path : str
            データベースファイルのパス
        """
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        setup_logging()

    def get_connection(self):
        """データベース接続を取得"""
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

    def execute_query(self, query, params=None):
        """
        SQLクエリを実行
        
        Parameters:
        -----------
        query : str
            実行するSQLクエリ
        params : tuple, optional
            クエリパラメータ
        
        Returns:
        --------
        list
            クエリ結果
        """
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
        """
        複数のSQLクエリを実行
        
        Parameters:
        -----------
        query : str
            実行するSQLクエリ
        params_list : list of tuple
            クエリパラメータのリスト
        """
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
