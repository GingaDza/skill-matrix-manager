"""初期スキーママイグレーション"""
VERSION = "V1"
NAME = "初期スキーマの作成"

def up():
    """マイグレーション実行"""
    return """
        -- ユーザーテーブル
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- グループテーブル
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- カテゴリーテーブル
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            group_id INTEGER NOT NULL,
            parent_id INTEGER,
            display_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
            FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL,
            UNIQUE(name, group_id)
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
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
            UNIQUE(name, category_id),
            CHECK (min_level >= 1 AND min_level <= max_level AND max_level <= 5)
        );

        -- ユーザースキルテーブル
        CREATE TABLE IF NOT EXISTS user_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            level INTEGER NOT NULL,
            achieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE,
            UNIQUE(user_id, skill_id),
            CHECK (level >= 1 AND level <= 5)
        );
    """

def down():
    """ロールバック実行"""
    return """
        DROP TABLE IF EXISTS user_skills;
        DROP TABLE IF EXISTS skills;
        DROP TABLE IF EXISTS categories;
        DROP TABLE IF EXISTS groups;
        DROP TABLE IF EXISTS users;
    """
