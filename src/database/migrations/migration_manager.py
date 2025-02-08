"""マイグレーション管理クラス"""
import os
import sqlite3
import logging
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

class MigrationManager:
    """マイグレーション管理クラス"""
    
    def __init__(self, db_path: str = "skill_matrix.db"):
        self.logger = logging.getLogger(__name__)
        self._db_path = db_path
        self._migrations_table = "migrations"
        self._init_migrations_table()
    
    def _init_migrations_table(self):
        """マイグレーションテーブルを初期化"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self._migrations_table} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        version TEXT UNIQUE NOT NULL,
                        name TEXT NOT NULL,
                        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
        except Exception as e:
            self.logger.exception("マイグレーションテーブルの初期化に失敗しました")
            raise
    
    def get_applied_migrations(self) -> List[str]:
        """適用済みのマイグレーション一覧を取得"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT version FROM {self._migrations_table} ORDER BY version")
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            self.logger.exception("適用済みマイグレーションの取得に失敗しました")
            raise
    
    def apply_migration(self, version: str, name: str, up_sql: str):
        """マイグレーションを適用"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.executescript(up_sql)
                cursor.execute(
                    f"INSERT INTO {self._migrations_table} (version, name) VALUES (?, ?)",
                    (version, name)
                )
                conn.commit()
                self.logger.info(f"マイグレーション {version} を適用しました: {name}")
        except Exception as e:
            self.logger.exception(f"マイグレーション {version} の適用に失敗しました: {name}")
            raise
    
    def rollback_migration(self, version: str, down_sql: str):
        """マイグレーションをロールバック"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.executescript(down_sql)
                cursor.execute(
                    f"DELETE FROM {self._migrations_table} WHERE version = ?",
                    (version,)
                )
                conn.commit()
                self.logger.info(f"マイグレーション {version} をロールバックしました")
        except Exception as e:
            self.logger.exception(f"マイグレーション {version} のロールバックに失敗しました")
            raise
