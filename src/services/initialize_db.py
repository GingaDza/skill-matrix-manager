import os
import sqlite3
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_tables(cursor):
    cursor.executescript('''
    -- 部門テーブル
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        created_at TEXT DEFAULT (DATETIME('now')),
        created_by TEXT NOT NULL,
        updated_at TEXT DEFAULT (DATETIME('now')),
        updated_by TEXT NOT NULL
    );

    -- 従業員テーブル
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        department_id INTEGER,
        created_at TEXT DEFAULT (DATETIME('now')),
        created_by TEXT NOT NULL,
        updated_at TEXT DEFAULT (DATETIME('now')),
        updated_by TEXT NOT NULL,
        FOREIGN KEY (department_id) REFERENCES departments(id)
    );

    -- スキルカテゴリテーブル
    CREATE TABLE IF NOT EXISTS skill_categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        parent_id INTEGER,
        created_at TEXT DEFAULT (DATETIME('now')),
        created_by TEXT NOT NULL,
        updated_at TEXT DEFAULT (DATETIME('now')),
        updated_by TEXT NOT NULL,
        FOREIGN KEY (parent_id) REFERENCES skill_categories(id)
    );

    -- スキルテーブル
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        category_id INTEGER NOT NULL,
        created_at TEXT DEFAULT (DATETIME('now')),
        created_by TEXT NOT NULL,
        updated_at TEXT DEFAULT (DATETIME('now')),
        updated_by TEXT NOT NULL,
        FOREIGN KEY (category_id) REFERENCES skill_categories(id)
    );

    -- スキル評価レベルテーブル
    CREATE TABLE IF NOT EXISTS skill_levels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        level_value INTEGER NOT NULL,
        created_at TEXT DEFAULT (DATETIME('now')),
        created_by TEXT NOT NULL,
        updated_at TEXT DEFAULT (DATETIME('now')),
        updated_by TEXT NOT NULL
    );

    -- 従業員スキル評価テーブル
    CREATE TABLE IF NOT EXISTS employee_skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        skill_id INTEGER NOT NULL,
        skill_level_id INTEGER NOT NULL,
        evaluation_date TEXT NOT NULL,
        comments TEXT,
        created_at TEXT DEFAULT (DATETIME('now')),
        created_by TEXT NOT NULL,
        updated_at TEXT DEFAULT (DATETIME('now')),
        updated_by TEXT NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES employees(id),
        FOREIGN KEY (skill_id) REFERENCES skills(id),
        FOREIGN KEY (skill_level_id) REFERENCES skill_levels(id),
        UNIQUE(employee_id, skill_id, evaluation_date)
    );
    ''')

def insert_initial_data(cursor, current_user):
    current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    # 部門データ
    departments = [
        ('開発部',),
        ('営業部',),
        ('管理部',),
        ('人事部',),
    ]
    cursor.executemany(
        'INSERT OR IGNORE INTO departments (name, created_by, updated_by) VALUES (?, ?, ?)',
        [(dept[0], current_user, current_user) for dept in departments]
    )

    # スキルレベル
    skill_levels = [
        ('初級', '基本的な知識がある', 1),
        ('中級', '実務で使用できる', 2),
        ('上級', '他者に指導できる', 3),
        ('エキスパート', '社内のエキスパート', 4),
    ]
    cursor.executemany(
        'INSERT OR IGNORE INTO skill_levels (name, description, level_value, created_by, updated_by) VALUES (?, ?, ?, ?, ?)',
        [(level[0], level[1], level[2], current_user, current_user) for level in skill_levels]
    )

    # スキルカテゴリ
    categories = [
        ('プログラミング言語', 'プログラミング言語に関するスキル'),
        ('フレームワーク', '各種フレームワークに関するスキル'),
        ('データベース', 'データベースに関するスキル'),
        ('開発ツール', '開発ツールに関するスキル'),
    ]
    cursor.executemany(
        'INSERT OR IGNORE INTO skill_categories (name, description, created_by, updated_by) VALUES (?, ?, ?, ?)',
        [(cat[0], cat[1], current_user, current_user) for cat in categories]
    )

def initialize_database(current_user='GingaDza'):
    db_path = 'skillmatrix.db'
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # テーブル作成
        create_tables(cursor)
        logger.info("Tables created successfully")
        
        # 初期データ投入
        insert_initial_data(cursor, current_user)
        logger.info("Initial data inserted successfully")
        
        conn.commit()
        
        # 作成されたテーブルの確認
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        logger.info(f"Available tables: {[table[0] for table in tables]}")
        
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    initialize_database()
