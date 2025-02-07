import sqlite3
import logging
from pathlib import Path
import os

class DatabaseManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_path = Path('data/skill_matrix.db')
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 既存のDBファイルを削除して新規作成
        if self.db_path.exists():
            os.remove(self.db_path)
            
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.current_user = "GingaDza"
        self.current_time = "2025-02-07 12:37:59"
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
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT NOT NULL
        )
        ''')

        # ユーザーテーブル
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            group_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT NOT NULL,
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
            created_by TEXT NOT NULL,
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
            created_by TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
        )
        ''')

    def _insert_initial_data(self):
        """初期データの挿入"""
        try:
            # デフォルトグループの作成
            self.cursor.execute('''
                INSERT INTO groups (name, created_at, created_by)
                VALUES (?, ?, ?)
            ''', ('デフォルトグループ', self.current_time, self.current_user))

            # デフォルトカテゴリーの作成
            self.cursor.execute('''
                INSERT INTO categories (name, parent_id, is_skill, created_at, created_by)
                VALUES (?, NULL, 0, ?, ?)
            ''', ('基本スキル', self.current_time, self.current_user))

            # デフォルトユーザーの作成
            default_group_id = self.cursor.lastrowid
            self.cursor.execute('''
                INSERT INTO users (name, group_id, created_at, created_by)
                VALUES (?, ?, ?, ?)
            ''', (self.current_user, default_group_id, self.current_time, self.current_user))

            self.conn.commit()
        except sqlite3.IntegrityError as e:
            self.logger.warning(f"初期データの挿入中に重複が検出されました: {e}")
        except Exception as e:
            self.logger.error(f"初期データの挿入中にエラーが発生: {e}")
            raise

    # ... 他のメソッドは変更なし ...

    def __del__(self):
        """デストラクタ：接続のクローズ"""
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
