from src.services.db import Database
import sqlite3
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_database():
    try:
        db = Database.get_instance()
        conn = db.get_connection()
        cursor = conn.cursor()

        # テーブル作成
        cursor.executescript('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            department_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        );

        CREATE TABLE IF NOT EXISTS skill_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            parent_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_id) REFERENCES skill_categories(id)
        );

        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES skill_categories(id)
        );

        CREATE TABLE IF NOT EXISTS skill_levels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            level_value INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS employee_skills (
            employee_id INTEGER,
            skill_id INTEGER,
            skill_level_id INTEGER,
            evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            evaluator TEXT,
            comments TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (employee_id, skill_id),
            FOREIGN KEY (employee_id) REFERENCES employees(id),
            FOREIGN KEY (skill_id) REFERENCES skills(id),
            FOREIGN KEY (skill_level_id) REFERENCES skill_levels(id)
        );
        ''')

        # サンプルデータの挿入
        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        # 部門データ
        cursor.executescript(f'''
        INSERT INTO departments (name, created_at, updated_at) VALUES 
        ('開発部', '{current_time}', '{current_time}'),
        ('営業部', '{current_time}', '{current_time}'),
        ('管理部', '{current_time}', '{current_time}');
        ''')

        # スキルレベル
        cursor.executescript(f'''
        INSERT INTO skill_levels (name, description, level_value, created_at, updated_at) VALUES 
        ('初級', '基本的な知識を持っている', 1, '{current_time}', '{current_time}'),
        ('中級', '実務で使用できる', 2, '{current_time}', '{current_time}'),
        ('上級', '他者に指導できる', 3, '{current_time}', '{current_time}'),
        ('エキスパート', '社内のエキスパート', 4, '{current_time}', '{current_time}');
        ''')

        # スキルカテゴリ
        cursor.executescript(f'''
        INSERT INTO skill_categories (name, description, created_at, updated_at) VALUES 
        ('プログラミング言語', 'プログラミング言語に関するスキル', '{current_time}', '{current_time}'),
        ('フレームワーク', '各種フレームワークに関するスキル', '{current_time}', '{current_time}'),
        ('ツール', '開発ツールに関するスキル', '{current_time}', '{current_time}');
        ''')

        # スキル
        cursor.executescript(f'''
        INSERT INTO skills (name, category_id, created_at, updated_at) 
        SELECT 'Python', id, '{current_time}', '{current_time}' FROM skill_categories WHERE name = 'プログラミング言語'
        UNION ALL
        SELECT 'Java', id, '{current_time}', '{current_time}' FROM skill_categories WHERE name = 'プログラミング言語'
        UNION ALL
        SELECT 'Spring Boot', id, '{current_time}', '{current_time}' FROM skill_categories WHERE name = 'フレームワーク'
        UNION ALL
        SELECT 'Django', id, '{current_time}', '{current_time}' FROM skill_categories WHERE name = 'フレームワーク'
        UNION ALL
        SELECT 'Git', id, '{current_time}', '{current_time}' FROM skill_categories WHERE name = 'ツール';
        ''')

        conn.commit()
        logger.info("Database initialized successfully")
        
        # 作成されたテーブルの確認
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        logger.info(f"Created tables: {tables}")

    except sqlite3.Error as e:
        logger.error(f"Error initializing database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    initialize_database()