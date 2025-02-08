"""アプリケーションのメインモジュール"""
from typing import Type
from .database.interfaces import IDataManager
from .database.database_manager import DatabaseManager
from .views.main_window import MainWindow

class App:
    """アプリケーションクラス"""
    
    def __init__(self, db_manager_class: Type[IDataManager] = DatabaseManager):
        """
        初期化
        
        Args:
            db_manager_class: データベースマネージャーのクラス
        """
        self._db = db_manager_class()
        self._init_main_window()
