"""アプリケーションのメインモジュール"""
import sys
import logging
from typing import List
from .utils.display import display_manager
from .database import DatabaseManager

class App:
    """アプリケーションクラス"""
    
    def __init__(self, argv: List[str]):
        """初期化"""
        self.logger = logging.getLogger(__name__)
        self.logger.info("アプリケーションを初期化中...")
        display_manager.show_info()
        self._db = DatabaseManager()
    
    def run(self):
        """アプリケーションを実行"""
        try:
            self.logger.info("アプリケーションを実行中...")
        except Exception as e:
            self.logger.exception("予期せぬエラーが発生しました")
            raise
