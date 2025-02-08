"""データベース基本管理クラス"""
import sqlite3
import logging
from typing import Any

class BaseManager:
    """データベース基本管理クラス"""
    
    def __init__(self, db_path: str = "skill_matrix.db"):
        """初期化"""
        self.logger = logging.getLogger(__name__)
        self._db_path = db_path

    def _execute(self, query: str, params: tuple = (), commit: bool = False) -> Any:
        """SQLクエリを実行"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                if commit:
                    conn.commit()
                    return cursor.rowcount
                return cursor.fetchall()
        except Exception as e:
            self.logger.exception("SQL実行エラー: %s", query)
            raise
