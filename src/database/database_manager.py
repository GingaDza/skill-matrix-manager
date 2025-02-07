import sqlite3
import logging
import os
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path="data/skill_matrix.db"):
        self.db_path = db_path
        # データベースファイルが存在する場合は削除（開発環境用）
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        # データディレクトリが存在しない場合は作成
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.setup_database()
        logger.debug(f"DatabaseManager initialized with path: {db_path}")

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def setup_database(self):
        """データベースの初期設定"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # グループテーブル
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS groups (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # ユーザーテーブル
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT,
                        group_id INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (group_id) REFERENCES groups(id)
                        ON DELETE SET NULL
                    )
                """)

                # カテゴリーテーブル
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS categories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # スキルテーブル
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS skills (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category_id INTEGER,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (category_id) REFERENCES categories(id)
                        ON DELETE CASCADE,
                        UNIQUE(name, category_id)
                    )
                """)

                # スキル評価テーブル
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS skill_evaluations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        skill_id INTEGER,
                        level INTEGER CHECK (level BETWEEN 0 AND 5),
                        evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                        ON DELETE CASCADE,
                        FOREIGN KEY (skill_id) REFERENCES skills(id)
                        ON DELETE CASCADE,
                        UNIQUE(user_id, skill_id)
                    )
                """)

                # サンプルデータの挿入
                cursor.execute("INSERT INTO groups (name) VALUES (?)", ("開発部",))
                cursor.execute("INSERT INTO groups (name) VALUES (?)", ("営業部",))
                cursor.execute("INSERT INTO groups (name) VALUES (?)", ("管理部",))
                
                cursor.execute("INSERT INTO categories (name) VALUES (?)", ("プログラミング",))
                cursor.execute("INSERT INTO categories (name) VALUES (?)", ("データベース",))
                cursor.execute("INSERT INTO categories (name) VALUES (?)", ("ネットワーク",))

                # スキルのサンプルデータ
                programming_id = cursor.execute("SELECT id FROM categories WHERE name = ?", ("プログラミング",)).fetchone()[0]
                database_id = cursor.execute("SELECT id FROM categories WHERE name = ?", ("データベース",)).fetchone()[0]
                network_id = cursor.execute("SELECT id FROM categories WHERE name = ?", ("ネットワーク",)).fetchone()[0]

                # プログラミングスキル
                cursor.execute("INSERT INTO skills (name, category_id, description) VALUES (?, ?, ?)",
                             ("Python", programming_id, "Pythonプログラミング言語"))
                cursor.execute("INSERT INTO skills (name, category_id, description) VALUES (?, ?, ?)",
                             ("Java", programming_id, "Javaプログラミング言語"))

                # データベーススキル
                cursor.execute("INSERT INTO skills (name, category_id, description) VALUES (?, ?, ?)",
                             ("SQL", database_id, "SQL言語"))
                cursor.execute("INSERT INTO skills (name, category_id, description) VALUES (?, ?, ?)",
                             ("MongoDB", database_id, "MongoDBデータベース"))

                # ネットワークスキル
                cursor.execute("INSERT INTO skills (name, category_id, description) VALUES (?, ?, ?)",
                             ("TCP/IP", network_id, "TCP/IPプロトコル"))
                cursor.execute("INSERT INTO skills (name, category_id, description) VALUES (?, ?, ?)",
                             ("セキュリティ", network_id, "ネットワークセキュリティ"))

                # ユーザーの追加
                cursor.execute("""
                    INSERT INTO users (name, email, group_id)
                    VALUES (?, ?, ?)
                """, ("山田太郎", "yamada@example.com", 1))

                conn.commit()
                logger.debug("Database tables and sample data created successfully")
        except Exception as e:
            logger.error(f"Error setting up database: {str(e)}")
            raise

    def get_all_categories_with_skills(self):
        """カテゴリーとそれに属するスキルを取得"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 
                        c.id as category_id, 
                        c.name as category_name,
                        s.id as skill_id,
                        s.name as skill_name,
                        s.description as skill_description
                    FROM categories c
                    LEFT JOIN skills s ON c.id = s.category_id
                    ORDER BY c.name, s.name
                """)
                
                categories = {}
                for row in cursor.fetchall():
                    category_id, category_name, skill_id, skill_name, skill_description = row
                    
                    if category_id not in categories:
                        categories[category_id] = (category_id, category_name, [])
                    
                    if skill_id is not None:
                        categories[category_id][2].append((skill_id, skill_name, skill_description))
                
                logger.debug(f"Retrieved {len(categories)} categories with skills")
                return list(categories.values())
        except Exception as e:
            logger.error(f"Error getting categories with skills: {str(e)}")
            raise

    def get_all_groups(self):
        """全グループを取得"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT g.id, g.name, COUNT(u.id) as user_count 
                    FROM groups g 
                    LEFT JOIN users u ON g.id = u.group_id 
                    GROUP BY g.id, g.name
                    ORDER BY g.name
                """)
                groups = cursor.fetchall()
                logger.debug(f"Retrieved {len(groups)} groups")
                return groups
        except Exception as e:
            logger.error(f"Error getting groups: {str(e)}")
            raise

    def add_group(self, name):
        """グループを追加"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO groups (name) VALUES (?)", (name,))
                group_id = cursor.lastrowid
                logger.debug(f"Added group: {name} (ID: {group_id})")
                return group_id
        except sqlite3.IntegrityError:
            logger.error(f"Group name already exists: {name}")
            raise ValueError(f"グループ名 '{name}' は既に存在します")
        except Exception as e:
            logger.error(f"Error adding group: {str(e)}")
            raise

    def update_group(self, group_id, new_name):
        """グループ名を更新"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE groups SET name = ? WHERE id = ?",
                    (new_name, group_id)
                )
                if cursor.rowcount == 0:
                    raise ValueError("グループが見つかりません")
                logger.debug(f"Updated group {group_id} to: {new_name}")
        except sqlite3.IntegrityError:
            logger.error(f"Group name already exists: {new_name}")
            raise ValueError(f"グループ名 '{new_name}' は既に存在します")
        except Exception as e:
            logger.error(f"Error updating group: {str(e)}")
            raise

    def delete_group(self, group_id):
        """グループを削除"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE group_id = ?", (group_id,))
                cursor.execute("DELETE FROM groups WHERE id = ?", (group_id,))
                if cursor.rowcount == 0:
                    raise ValueError("グループが見つかりません")
                logger.debug(f"Deleted group: {group_id}")
        except Exception as e:
            logger.error(f"Error deleting group: {str(e)}")
            raise

    def get_all_categories(self):
        """全カテゴリーを取得"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name FROM categories ORDER BY name")
                categories = cursor.fetchall()
                logger.debug(f"Retrieved {len(categories)} categories")
                return categories
        except Exception as e:
            logger.error(f"Error getting categories: {str(e)}")
            raise

    def add_category(self, name):
        """カテゴリーを追加"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
                category_id = cursor.lastrowid
                logger.debug(f"Added category: {name} (ID: {category_id})")
                return category_id
        except sqlite3.IntegrityError:
            logger.error(f"Category name already exists: {name}")
            raise ValueError(f"カテゴリー名 '{name}' は既に存在します")
        except Exception as e:
            logger.error(f"Error adding category: {str(e)}")
            raise

    def update_category(self, category_id, new_name):
        """カテゴリー名を更新"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE categories SET name = ? WHERE id = ?",
                    (new_name, category_id)
                )
                if cursor.rowcount == 0:
                    raise ValueError("カテゴリーが見つかりません")
                logger.debug(f"Updated category {category_id} to: {new_name}")
        except sqlite3.IntegrityError:
            logger.error(f"Category name already exists: {new_name}")
            raise ValueError(f"カテゴリー名 '{new_name}' は既に存在します")
        except Exception as e:
            logger.error(f"Error updating category: {str(e)}")
            raise

    def delete_category(self, category_id):
        """カテゴリーを削除"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM skills WHERE category_id = ?", (category_id,))
                cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
                if cursor.rowcount == 0:
                    raise ValueError("カテゴリーが見つかりません")
                logger.debug(f"Deleted category: {category_id}")
        except Exception as e:
            logger.error(f"Error deleting category: {str(e)}")
            raise

    def add_skill(self, name, category_id, description=None):
        """スキルを追加"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO skills (name, category_id, description) VALUES (?, ?, ?)",
                    (name, category_id, description)
                )
                skill_id = cursor.lastrowid
                logger.debug(f"Added skill: {name} (ID: {skill_id})")
                return skill_id
        except sqlite3.IntegrityError:
            logger.error(f"Skill name already exists in category: {name}")
            raise ValueError(f"スキル名 '{name}' は既にこのカテゴリーに存在します")
        except Exception as e:
            logger.error(f"Error adding skill: {str(e)}")
            raise

    def get_users_by_group(self, group_id):
        """指定されたグループのユーザーを取得"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, name, email
                    FROM users
                    WHERE group_id = ?
                    ORDER BY name
                """, (group_id,))
                users = cursor.fetchall()
                logger.debug(f"Retrieved {len(users)} users for group {group_id}")
                return users
        except Exception as e:
            logger.error(f"Error getting users by group: {str(e)}")
            raise
