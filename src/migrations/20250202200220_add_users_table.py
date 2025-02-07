# src/desktop/migrations/20250202200220_add_users_table.py

def upgrade(cursor):
    """ユーザーテーブルを作成"""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # トリガーを作成して updated_at を自動更新
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS users_updated_at
        AFTER UPDATE ON users
        FOR EACH ROW
        BEGIN
            UPDATE users SET updated_at = CURRENT_TIMESTAMP
            WHERE id = OLD.id;
        END;
    """)

def downgrade(cursor):
    """ユーザーテーブルを削除"""
    cursor.execute("DROP TRIGGER IF EXISTS users_updated_at")
    cursor.execute("DROP TABLE IF EXISTS users")