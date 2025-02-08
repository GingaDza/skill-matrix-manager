"""初期スキーママイグレーション"""
from datetime import datetime

VERSION = "V1"
NAME = "初期スキーマの作成"

def up():
    """マイグレーション実行"""
    return """
        -- グループテーブル
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- カテゴリーテーブル
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            group_id INTEGER NOT NULL,
            parent_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(name, group_id),
            FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
            FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
        );

        -- スキルテーブル
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category_id INTEGER NOT NULL,
            min_level INTEGER DEFAULT 1,
            max_level INTEGER DEFAULT 5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(name, category_id),
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
            CHECK (min_level >= 1 AND min_level <= max_level AND max_level <= 5)
        );
    """

def down():
    """ロールバック実行"""
    return """
        DROP TABLE IF EXISTS skills;
        DROP TABLE IF EXISTS categories;
        DROP TABLE IF EXISTS groups;
    """
