import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

class Database:
    """データベース管理クラス"""
    
    def __init__(self, db_path: str = "skill_matrix.db"):
        self.db_path = db_path
        self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._setup_database()
        
    def _setup_database(self):
        """データベースのセットアップ"""
        try:
            # データベースディレクトリの作成
            db_dir = Path(self.db_path).parent
            db_dir.mkdir(parents=True, exist_ok=True)
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # グループテーブルの作成
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS groups (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                ''')
                
                # ユーザーテーブルの作成
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        employee_id TEXT NOT NULL UNIQUE,
                        name TEXT NOT NULL,
                        group_id INTEGER,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,
                        FOREIGN KEY (group_id) REFERENCES groups (id)
                            ON DELETE SET NULL
                            ON UPDATE CASCADE
                    )
                ''')
                
                # スキルカテゴリーテーブルの作成
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS skill_categories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        description TEXT,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                ''')
                
                # スキルテーブルの作成
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS skills (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category_id INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        description TEXT,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,
                        FOREIGN KEY (category_id) REFERENCES skill_categories (id)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE,
                        UNIQUE (category_id, name)
                    )
                ''')
                
                # ユーザースキルテーブルの作成
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_skills (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        skill_id INTEGER NOT NULL,
                        level INTEGER NOT NULL CHECK (level BETWEEN 0 AND 5),
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE,
                        FOREIGN KEY (skill_id) REFERENCES skills (id)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE,
                        UNIQUE (user_id, skill_id)
                    )
                ''')
                
                conn.commit()
                logger.info(f"{self.current_time} - Database tables created successfully")
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to setup database: {str(e)}")
            raise
            
    def get_connection(self) -> sqlite3.Connection:
        """データベース接続を取得"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # 行を辞書形式で取得
            return conn
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get database connection: {str(e)}")
            raise
            
    def execute_migration(self, migration_sql: str) -> bool:
        """マイグレーションを実行"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.executescript(migration_sql)
                conn.commit()
                logger.info(f"{self.current_time} - Migration executed successfully")
                return True
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to execute migration: {str(e)}")
            return False
            
    def get_table_info(self, table_name: str) -> list:
        """テーブルの構造情報を取得"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"PRAGMA table_info({table_name})")
                return cursor.fetchall()
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get table info: {str(e)}")
            raise
            
    def backup_database(self, backup_path: Optional[str] = None) -> bool:
        """データベースのバックアップを作成"""
        try:
            if backup_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"backup_{timestamp}.db"
                
            with self.get_connection() as source_conn:
                backup_conn = sqlite3.connect(backup_path)
                source_conn.backup(backup_conn)
                backup_conn.close()
                
            logger.info(f"{self.current_time} - Database backup created: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to backup database: {str(e)}")
            return False