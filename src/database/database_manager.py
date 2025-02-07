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
        self.current_time = "2025-02-07 14:16:28"
        self.initialize_database()

    def initialize_database(self):
        """データベースの初期化とテストデータの挿入"""
        try:
            # テーブル作成
            self.create_tables()
            
            # テストデータ挿入
            self.insert_test_data()
            
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

        # カテゴリーテーブル
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            parent_id INTEGER,
            group_id INTEGER,
            is_skill BOOLEAN DEFAULT 0,
            created_at DATETIME NOT NULL,
            created_by TEXT NOT NULL,
            FOREIGN KEY (parent_id) REFERENCES categories (id) ON DELETE CASCADE,
            FOREIGN KEY (group_id) REFERENCES groups (id) ON DELETE CASCADE
        )
        ''')

    def insert_test_data(self):
        """テストデータの挿入"""
        try:
            # テストグループの作成
            test_groups = [
                "開発部門",
                "デザイン部門",
                "マーケティング部門"
            ]
            
            for group in test_groups:
                self.cursor.execute('''
                    INSERT INTO groups (name, created_at, created_by)
                    VALUES (?, ?, ?)
                ''', (group, self.current_time, self.current_user))
                
                group_id = self.cursor.lastrowid
                
                # 各グループのテストカテゴリー
                test_categories = [
                    f"{group} - 基礎スキル",
                    f"{group} - 応用スキル",
                    f"{group} - 専門スキル"
                ]
                
                for category in test_categories:
                    self.cursor.execute('''
                        INSERT INTO categories (name, group_id, is_skill, created_at, created_by)
                        VALUES (?, ?, 0, ?, ?)
                    ''', (category, group_id, self.current_time, self.current_user))
                    
                    category_id = self.cursor.lastrowid
                    
                    # 各カテゴリーのテストスキル
                    test_skills = [
                        f"{category} - レベル1",
                        f"{category} - レベル2",
                        f"{category} - レベル3"
                    ]
                    
                    for skill in test_skills:
                        self.cursor.execute('''
                            INSERT INTO categories (name, parent_id, group_id, is_skill, created_at, created_by)
                            VALUES (?, ?, ?, 1, ?, ?)
                        ''', (skill, category_id, group_id, self.current_time, self.current_user))

            self.conn.commit()
            self.logger.info("テストデータの挿入が完了しました")
        except Exception as e:
            self.logger.error(f"テストデータの挿入中にエラーが発生: {e}")
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

    def get_categories_by_group(self, group_id):
        """グループに属するカテゴリーを取得"""
        try:
            self.cursor.execute('''
                SELECT id, name 
                FROM categories 
                WHERE group_id = ? AND is_skill = 0 
                ORDER BY name
            ''', (group_id,))
            return self.cursor.fetchall()
        except Exception as e:
            self.logger.error(f"カテゴリー取得中にエラーが発生: {e}")
            return []

    def get_skills_by_category(self, category_id):
        """カテゴリーに属するスキルを取得"""
        try:
            self.cursor.execute('''
                SELECT id, name 
                FROM categories 
                WHERE parent_id = ? AND is_skill = 1 
                ORDER BY name
            ''', (category_id,))
            return self.cursor.fetchall()
        except Exception as e:
            self.logger.error(f"スキル取得中にエラーが発生: {e}")
            return []

    # ... [その他のメソッドは変更なし]
