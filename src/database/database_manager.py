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
        self.current_time = "2025-02-07 13:51:17"  # 時刻を更新
        self.initialize_database()

    def initialize_database(self):
        """データベースの初期化"""
        self.logger.info("データベースの初期化を開始")
        try:
            self.create_tables()
            self.insert_initial_data()
            self.conn.commit()
            self.logger.info("データベースの初期化が完了しました")
        except Exception as e:
            self.logger.error(f"データベースの初期化中にエラーが発生: {e}")
            raise

    def create_tables(self):
        """テーブルの作成"""
        # グループテーブル
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at DATETIME NOT NULL,
            created_by TEXT NOT NULL
        )
        ''')

        # ユーザーテーブル
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            group_id INTEGER,
            created_at DATETIME NOT NULL,
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
            created_at DATETIME NOT NULL,
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
            created_at DATETIME NOT NULL,
            created_by TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
        )
        ''')

    def insert_initial_data(self):
        """初期データの挿入"""
        try:
            # デフォルトグループの作成
            self.cursor.execute('''
                INSERT INTO groups (name, created_at, created_by)
                VALUES (?, ?, ?)
            ''', ('デフォルトグループ', self.current_time, self.current_user))

            default_group_id = self.cursor.lastrowid

            # デフォルトカテゴリーの作成
            self.cursor.execute('''
                INSERT INTO categories (name, parent_id, is_skill, created_at, created_by)
                VALUES (?, NULL, 0, ?, ?)
            ''', ('基本スキル', self.current_time, self.current_user))

            # デフォルトユーザーの作成
            self.cursor.execute('''
                INSERT INTO users (name, group_id, created_at, created_by)
                VALUES (?, ?, ?, ?)
            ''', (self.current_user, default_group_id, self.current_time, self.current_user))

            self.conn.commit()
        except sqlite3.IntegrityError as e:
            self.logger.warning(f"初期データの挿入中に重複が検出されました: {e}")
            self.conn.rollback()
        except Exception as e:
            self.logger.error(f"初期データの挿入中にエラーが発生: {e}")
            self.conn.rollback()
            raise

    def get_all_groups(self):
        """全グループを取得"""
        try:
            self.cursor.execute('SELECT id, name FROM groups ORDER BY name')
            return self.cursor.fetchall()
        except Exception as e:
            self.logger.error(f"グループ取得中にエラーが発生: {e}")
            return []

    def get_group(self, group_id):
        """グループ情報を取得"""
        try:
            self.cursor.execute('SELECT id, name FROM groups WHERE id = ?', (group_id,))
            return self.cursor.fetchone()
        except Exception as e:
            self.logger.error(f"グループ取得中にエラーが発生: {e}")
            return None

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
                WHERE is_skill = 0 
                ORDER BY name
            ''')
            parent_categories = self.cursor.fetchall()

            result = []
            for parent in parent_categories:
                # 子カテゴリー（スキル）の取得
                self.cursor.execute('''
                    SELECT id, name FROM categories 
                    WHERE parent_id = ? AND is_skill = 1
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
            self.cursor.execute(
                'INSERT INTO groups (name, created_at, created_by) VALUES (?, ?, ?)',
                (name, self.current_time, self.current_user)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            self.logger.error(f"グループ追加中にエラーが発生: {e}")
            return None

    def edit_group(self, group_id, name):
        """グループを編集"""
        try:
            self.cursor.execute(
                'UPDATE groups SET name = ?, created_at = ?, created_by = ? WHERE id = ?',
                (name, self.current_time, self.current_user, group_id)
            )
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"グループ編集中にエラーが発生: {e}")
            return False

    def delete_group(self, group_id):
        """グループを削除"""
        try:
            self.cursor.execute('DELETE FROM groups WHERE id = ?', (group_id,))
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"グループ削除中にエラーが発生: {e}")
            return False

    def add_category(self, name, parent_id=None, is_skill=False):
        """カテゴリーを追加"""
        try:
            self.cursor.execute(
                'INSERT INTO categories (name, parent_id, is_skill, created_at, created_by) VALUES (?, ?, ?, ?, ?)',
                (name, parent_id, is_skill, self.current_time, self.current_user)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            self.logger.error(f"カテゴリー追加中にエラーが発生: {e}")
            return None

    def edit_category(self, category_id, name):
        """カテゴリーを編集"""
        try:
            self.cursor.execute(
                'UPDATE categories SET name = ?, created_at = ?, created_by = ? WHERE id = ?',
                (name, self.current_time, self.current_user, category_id)
            )
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"カテゴリー編集中にエラーが発生: {e}")
            return False

    def delete_category(self, category_id):
        """カテゴリーを削除"""
        try:
            self.cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"カテゴリー削除中にエラーが発生: {e}")
            return False

    def __del__(self):
        """デストラクタ：接続のクローズ"""
        if hasattr(self, 'conn') and self.conn:
            try:
                self.conn.close()
            except Exception:
                pass
