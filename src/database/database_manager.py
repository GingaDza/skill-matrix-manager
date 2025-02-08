"""データベースマネージャークラス"""
from .base_manager import BaseManagerMixin

class DatabaseManager(BaseManagerMixin):
    """データベース操作を管理するクラス"""
    
    def __init__(self, db_path: str = "skill_matrix.db"):
        """
        初期化
        
        Args:
            db_path (str): データベースファイルのパス
        """
        super().__init__(db_path)