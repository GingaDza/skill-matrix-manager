"""データベースマネージャークラス"""
import logging
from pathlib import Path
from .migration_manager import MigrationManager

class DatabaseManager:
    """データベース操作を管理するクラス"""
    
    def __init__(self, db_path: str = "skill_matrix.db"):
        """
        初期化
        
        Args:
            db_path (str): データベースファイルのパス
        """
        self.logger = logging.getLogger(__name__)
        self.db_path = Path(db_path)
        
        # マイグレーションを実行
        migration_manager = MigrationManager(str(self.db_path))
        if not migration_manager.run_migrations():
            raise RuntimeError("データベースの初期化に失敗しました")
        
        # マイグレーション成功後、ベースマネージャーの機能をコピー
        for attr in dir(migration_manager):
            if not attr.startswith('_') and attr != 'run_migrations':
                setattr(self, attr, getattr(migration_manager, attr))