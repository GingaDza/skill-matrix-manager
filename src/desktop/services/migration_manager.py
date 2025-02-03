# src/desktop/services/migration_manager.py
import os
import sqlite3
import logging
from pathlib import Path
from typing import List, Tuple
from ..utils.time_utils import TimeProvider

logger = logging.getLogger(__name__)

class MigrationManager:
    """データベースマイグレーション管理クラス"""
    
    def __init__(self, db_path: str):
        self.current_time = TimeProvider.get_current_time()
        self.current_user = TimeProvider.get_current_user()
        self.db_path = db_path
        self.migrations_dir = Path(__file__).parent / 'migrations'
        
        # マイグレーションディレクトリが存在しない場合は作成
        os.makedirs(self.migrations_dir, exist_ok=True)
        
        # マイグレーション履歴テーブルの作成
        self._create_migrations_table()
        
        logger.debug(f"{self.current_time} - MigrationManager initialized with db_path: {db_path}")

    def _create_migrations_table(self):
        """マイグレーション履歴を管理するテーブルを作成"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS migrations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        version TEXT NOT NULL,
                        name TEXT NOT NULL,
                        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        applied_by TEXT
                    )
                """)
                conn.commit()
            logger.debug(f"{self.current_time} - Migrations table created")
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to create migrations table: {str(e)}")
            raise

    def _create_initial_migration(self):
        """初期マイグレーションファイルを作成"""
        migration_path = self.migrations_dir / '20250202083743_initial_schema.sql'
        
        if not migration_path.exists():
            with open(migration_path, 'w') as f:
                f.write("""-- Up migration
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT
);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    parent_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (parent_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS group_categories (
    group_id INTEGER,
    category_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    PRIMARY KEY (group_id, category_id),
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Down migration
DROP TABLE IF EXISTS group_categories;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS groups;
""")
            logger.info(f"{self.current_time} - Created initial migration file: {migration_path}")

    def get_applied_migrations(self) -> List[str]:
        """適用済みのマイグレーションバージョンを取得"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT version FROM migrations ORDER BY version")
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get applied migrations: {str(e)}")
            raise

    def get_pending_migrations(self) -> List[Tuple[str, Path]]:
        """未適用のマイグレーションファイルを取得"""
        try:
            # 初期マイグレーションファイルを作成
            self._create_initial_migration()
            
            applied = set(self.get_applied_migrations())
            pending = []
            
            # マイグレーションファイルをスキャン
            for file in sorted(self.migrations_dir.glob('*.sql')):
                version = file.stem.split('_')[0]
                if version not in applied:
                    pending.append((version, file))
            
            return pending
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get pending migrations: {str(e)}")
            raise

    def apply_migration(self, version: str, file_path: Path):
        """マイグレーションを適用"""
        try:
            # SQLファイルを読み込む
            with open(file_path, 'r') as f:
                sql = f.read()

            # Up migrationの部分を抽出
            up_sql = sql.split('-- Down migration')[0]

            with sqlite3.connect(self.db_path) as conn:
                # マイグレーションを実行
                conn.executescript(up_sql)
                
                # マイグレーション履歴を記録
                conn.execute(
                    "INSERT INTO migrations (version, name, applied_by) VALUES (?, ?, ?)",
                    (version, file_path.stem, self.current_user)
                )
                conn.commit()
                
            logger.info(f"{self.current_time} - Applied migration: {file_path.stem}")
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to apply migration {file_path.stem}: {str(e)}")
            raise

    def migrate(self):
        """全ての未適用マイグレーションを実行"""
        try:
            pending = self.get_pending_migrations()
            if not pending:
                logger.info(f"{self.current_time} - No pending migrations")
                return

            for version, file_path in pending:
                self.apply_migration(version, file_path)
                
            logger.info(f"{self.current_time} - Applied {len(pending)} migrations")
        except Exception as e:
            logger.error(f"{self.current_time} - Migration failed: {str(e)}")
            raise

    def reset(self):
        """マイグレーション履歴をリセット"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # 既存のテーブルを削除
                conn.execute("DROP TABLE IF EXISTS group_categories")
                conn.execute("DROP TABLE IF EXISTS categories")
                conn.execute("DROP TABLE IF EXISTS groups")
                conn.execute("DROP TABLE IF EXISTS migrations")
                conn.commit()
                
            # マイグレーション履歴テーブルを再作成
            self._create_migrations_table()
            
            logger.info(f"{self.current_time} - Migration history reset completed")
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to reset migrations: {str(e)}")
            raise