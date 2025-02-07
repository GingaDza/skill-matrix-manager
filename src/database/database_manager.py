import sqlite3
import logging
from pathlib import Path

class DatabaseManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_path = Path('data/skill_matrix.db')
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.initialize_database()

    def initialize_database(self):
        """データベースの初期化"""
        self.logger.info("データベースの初期化を開始")
        try:
            self._create_tables()
            self._insert_initial_data()
            self.conn.commit()
            self.logger.info("データベースの初期化が完了しました")
        except Exception as e:
            self.logger.error(f"データベースの初期化中にエラーが発生: {e}")
            raise

    def _create_tables(self):
        """テーブルの作成"""
        # グループテーブル
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # ユーザーテーブル
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            group_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_id) REFERENCES groups (id) ON DELETE SET NULL
        )
        ''')

        # カテゴリーテーブル
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            parent_id INTEGER,
            is_skill BOOLEAN DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_id) REFERENCES categories (id) ON DELETE CASCADE
        )
        ''')

        # スキルレベルテーブル
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS skill_levels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category_id INTEGER,
            level INTEGER CHECK (level BETWEEN 1 AND 5),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
        )
        ''')

    def get_group(self, group_id):
        """グループ情報を取得"""
        try:
            self.cursor.execute('SELECT id, name FROM groups WHERE id = ?', (group_id,))
            return self.cursor.fetchone()
        except Exception as e:
            self.logger.error(f"グループ取得中にエラーが発生: {e}")
            return None

    # ... 他のメソッドは変更なし ...

