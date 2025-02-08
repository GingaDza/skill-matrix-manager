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
        display_manager.show_app_header()
        self.logger.info("アプリケーションを初期化中...")
        
        try:
            self._db = DatabaseManager()
            display_manager.show_success("データベース接続が確立されました")
        except Exception as e:
            display_manager.show_error(f"データベース接続に失敗しました: {e}")
            raise
    
    def run(self):
        """アプリケーションを実行"""
        try:
            display_manager.show_section_header("メイン処理")
            self.logger.info("アプリケーションを実行中...")
            # アプリケーションのメイン処理
        except Exception as e:
            display_manager.show_error(f"実行中にエラーが発生しました: {e}")
            raise

