"""アプリケーションのメインモジュール"""
import sys
import logging
from typing import List
from .utils.display import display
from .database import DatabaseManager

class App:
    def __init__(self, argv: List[str]):
        self.logger = logging.getLogger(__name__)
        
        # アプリケーション情報を表示
        display.show_app_info()
        
        try:
            self._db = DatabaseManager()
            display.show_message("データベース接続が確立されました", "success")
        except Exception as e:
            display.show_message(f"データベース接続エラー: {e}", "error")
            raise
    
    def run(self):
        try:
            display.show_section("メイン処理")
            self.logger.info("アプリケーションを実行中...")
            # メイン処理をここに実装
        except Exception as e:
            display.show_message(f"実行エラー: {e}", "error")
            raise
