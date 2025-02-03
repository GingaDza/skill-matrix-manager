# src/desktop/services/db.py
import sqlite3
import os
import logging
from pathlib import Path
from .migration_manager import MigrationManager  # 追加
from ..utils.time_utils import TimeProvider

logger = logging.getLogger(__name__)

class DatabaseManager:
    """データベース管理クラス"""
    
    def __init__(self):
        self.current_time = TimeProvider.get_current_time()
        self.current_user = TimeProvider.get_current_user()
        
        # データベースファイルのパスを設定
        self.db_path = os.path.expanduser("~/.skill_matrix/skill_matrix.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        logger.debug(f"{self.current_time} - Database path set to: {self.db_path}")
        
        # マイグレーションマネージャーを初期化して実行
        migration_manager = MigrationManager(self.db_path)
        migration_manager.migrate()
        
        # データベース接続を確立
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        
        logger.info(f"{self.current_time} - Connected to database: {self.db_path}")

    def execute_query(self, query: str, params: tuple = ()) -> list:
        """
        SELECTクエリを実行
        
        Args:
            query (str): 実行するSQLクエリ
            params (tuple): クエリパラメータ
            
        Returns:
            list: クエリ結果
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to execute query: {str(e)}")
            raise

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """
        INSERT/UPDATE/DELETEクエリを実行
        
        Args:
            query (str): 実行するSQLクエリ
            params (tuple): クエリパラメータ
            
        Returns:
            int: 影響を受けた行数
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to execute update: {str(e)}")
            self.connection.rollback()
            raise

    def reset_database(self):
        """データベースをリセット"""
        try:
            # マイグレーション履歴をリセット
            migration_manager = MigrationManager(self.db_path)
            migration_manager.reset()
            
            # マイグレーションを再実行
            migration_manager.migrate()
            
            logger.info(f"{self.current_time} - Database reset completed")
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to reset database: {str(e)}")
            raise

    def __del__(self):
        """デストラクタ：接続を閉じる"""
        if hasattr(self, 'connection'):
            self.connection.close()