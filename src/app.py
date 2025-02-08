"""アプリケーションのメインモジュール"""
import sys
import logging
from typing import Type, List, Optional
from PyQt5.QtWidgets import QApplication

from .database.interfaces import IDataManager
from .database.database_manager import DatabaseManager
from .views.main_window import MainWindow

class App:
    """アプリケーションクラス"""
    
    def __init__(self, args: Optional[List[str]] = None, db_manager_class: Type[IDataManager] = DatabaseManager):
        """
        初期化
        
        Args:
            args: コマンドライン引数
            db_manager_class: データベースマネージャーのクラス
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info("アプリケーションを初期化中...")
        
        # データベースマネージャーの初期化
        self._db = db_manager_class()
        
        # QApplicationの初期化
        self._app = QApplication(args if args is not None else sys.argv)
        
        # メインウィンドウの初期化
        self._init_main_window()

    def _init_main_window(self):
        """メインウィンドウを初期化"""
        self._main_window = MainWindow(self._db)
        self._main_window.show()

    def run(self) -> int:
        """
        アプリケーションを実行
        
        Returns:
            int: 終了コード
        """
        return self._app.exec_()

    def cleanup(self):
        """アプリケーションのクリーンアップ処理"""
        self.logger.info("アプリケーションを終了します")
