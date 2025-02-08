"""アプリケーションのメインモジュール"""
import sys
import logging
from typing import List
from .config import Config
from .database import DatabaseManager
from .utils.logging_config import setup_logging
from .utils.display import display_info

class App:
    """アプリケーションのメインクラス"""
    
    def __init__(self, argv: List[str]):
        """初期化
        
        Args:
            argv: コマンドライン引数
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info("アプリケーションを初期化中...")
        
        # 設定を読み込み
        self.config = Config.from_env()
        
        # ロギングを設定
        setup_logging(self.config.log_dir)
        
        # タイムスタンプとユーザー情報を表示
        display_info()
        
        # データベースマネージャーを初期化
        self._db = DatabaseManager(self.config.db.path)
    
    def run(self):
        """アプリケーションを実行"""
        try:
            self.logger.info("アプリケーションを実行中...")
            # アプリケーションのメイン処理
            pass
        except Exception as e:
            self.logger.exception("予期せぬエラーが発生しました")
            raise
