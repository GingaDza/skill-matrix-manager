"""アプリケーションのメインモジュール"""
import sys
import logging
from typing import Type, List, Optional
from PyQt5.QtWidgets import QApplication, QWidget

from .database.interfaces import IDataManager
from .database.database_manager import DatabaseManager
from .views.main_window import MainWindow

class App:
    """アプリケーションクラス"""
    
    _instance = None
    _app = None
    
    def __new__(cls, *args, **kwargs):
        """シングルトンパターンの実装"""
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, args: Optional[List[str]] = None):
        """
        初期化
        
        Args:
            args: コマンドライン引数
        """
        if not App._app:
            # QApplicationの初期化（最初に行う）
            App._app = QApplication(args if args is not None else sys.argv)
            
            self.logger = logging.getLogger(__name__)
            self.logger.info("アプリケーションを初期化中...")
            
            # データベースマネージャーの初期化
            self._db = DatabaseManager()
            
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
        if App._app:
            return App._app.exec_()
        return 1

    def cleanup(self):
        """アプリケーションのクリーンアップ処理"""
        self.logger.info("アプリケーションを終了します")
