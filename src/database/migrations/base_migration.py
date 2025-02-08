"""ベースマイグレーションクラス"""
from abc import ABC, abstractmethod
import sqlite3
import logging
from typing import Any

class BaseMigration(ABC):
    """マイグレーションの基底クラス"""
    
    def __init__(self, db_path: str):
        self.logger = logging.getLogger(__name__)
        self._db_path = db_path
    
    @abstractmethod
    def up(self):
        """マイグレーションを実行"""
        pass
    
    @abstractmethod
    def down(self):
        """ロールバックを実行"""
        pass
    
    def _execute(self, query: str, params: tuple = ()) -> Any:
        """SQLクエリを実行"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.fetchall()
        except Exception as e:
            self.logger.exception("マイグレーションエラー: %s", query)
            raise
