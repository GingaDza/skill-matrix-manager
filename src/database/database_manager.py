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

    def _insert_initial_data(self):
        """初期データの挿入"""
        # 初期グループの作成
        try:
            self.cursor.execute('INSERT OR IGNORE INTO groups (name) VALUES (?)', ('デフォルトグループ',))
        except sqlite3.IntegrityError:
            pass

    def get_all_groups(self):
        """全グループを取得"""
        try:
            self.cursor.execute('SELECT id, name FROM groups ORDER BY name')
            return self.cursor.fetchall()
        except Exception as e:
            self.logger.error(f"グループ取得中にエラーが発生: {e}")
            return []

    def get_users_by_group(self, group_id):
        """指定されたグループのユーザーを取得"""
        try:
            self.cursor.execute(
                'SELECT id, name FROM users WHERE group_id = ? ORDER BY name',
                (group_id,)
            )
            return self.cursor.fetchall()
        except Exception as e:
            self.logger.error(f"ユーザー取得中にエラーが発生: {e}")
            return []

    def get_all_categories_with_skills(self):
        """全カテゴリーとスキルを取得"""
        try:
            # 親カテゴリーの取得
            self.cursor.execute('''
                SELECT id, name FROM categories 
                WHERE parent_id IS NULL 
                ORDER BY name
            ''')
            parent_categories = self.cursor.fetchall()

            result = []
            for parent in parent_categories:
                # 子カテゴリー（スキル）の取得
                self.cursor.execute('''
                    SELECT id, name FROM categories 
                    WHERE parent_id = ? 
                    ORDER BY name
                ''', (parent[0],))
                skills = self.cursor.fetchall()
                
                result.append({
                    'category': parent,
                    'skills': skills
                })
            return result
        except Exception as e:
            self.logger.error(f"カテゴリー取得中にエラーが発生: {e}")
            return []

    def add_group(self, name):
        """グループを追加"""
        try:
            self.cursor.execute('INSERT INTO groups (name) VALUES (?)', (name,))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            self.logger.error(f"グループ追加中にエラーが発生: {e}")
            return None

    def add_user(self, name, group_id):
        """ユーザーを追加"""
        try:
            self.cursor.execute(
                'INSERT INTO users (name, group_id) VALUES (?, ?)',
                (name, group_id)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            self.logger.error(f"ユーザー追加中にエラーが発生: {e}")
            return None

    def edit_user(self, user_id, name, group_id):
        """ユーザーを編集"""
        try:
            self.cursor.execute(
                'UPDATE users SET name = ?, group_id = ? WHERE id = ?',
                (name, group_id, user_id)
            )
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"ユーザー編集中にエラーが発生: {e}")
            return False

    def delete_user(self, user_id):
        """ユーザーを削除"""
        try:
            self.cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"ユーザー削除中にエラーが発生: {e}")
            return False

    def add_category(self, name, parent_id=None):
        """カテゴリーを追加"""
        try:
            self.cursor.execute(
                'INSERT INTO categories (name, parent_id) VALUES (?, ?)',
                (name, parent_id)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            self.logger.error(f"カテゴリー追加中にエラーが発生: {e}")
            return None

    def __del__(self):
        """デストラクタ：接続のクローズ"""
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
