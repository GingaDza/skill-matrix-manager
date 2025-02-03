# src/desktop/migrations/20250202195015_add_users_table.py
def upgrade(cursor):
    """
    ユーザーテーブルを作成
    """
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

def downgrade(cursor):
    """
    ユーザーテーブルを削除
    """
    cursor.execute("DROP TABLE IF EXISTS users")