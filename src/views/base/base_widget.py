"""ベースウィジェットクラス"""
import logging
from PyQt6.QtWidgets import QWidget
from typing import Optional, Any

class BaseWidget(QWidget):
    """全てのウィジェットの基底クラス"""
    
    def __init__(self, db_manager: Optional[Any] = None, parent: Optional[QWidget] = None):
        """
        初期化
        
        Args:
            db_manager: データベースマネージャー
            parent: 親ウィジェット
        """
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self._db_manager = db_manager

    def setup(self):
        """
        ウィジェットのセットアップを行う
        
        Note:
            1. UIの初期化
            2. 初期データの読み込み
            3. シグナルの接続
            の順で実行される
        """
        try:
            # UIの初期化
            self.init_ui()
            self.logger.info("UI initialized")
            
            # 初期データの読み込み（存在する場合）
            if hasattr(self, '_load_initial_data'):
                self._load_initial_data()
            
            # シグナルの接続
            if hasattr(self, '_connect_signals'):
                self._connect_signals()
                self.logger.info("Signals connected")
        
        except Exception as e:
            self.logger.exception("Setup failed")
            raise

    def init_ui(self):
        """UIを初期化する"""
        pass