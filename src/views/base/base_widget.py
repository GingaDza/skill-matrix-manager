"""ベースウィジェットクラス"""
import logging
from PyQt6.QtWidgets import QWidget

class BaseWidget(QWidget):
    """全てのウィジェットの基底クラス"""
    
    def __init__(self, parent=None):
        """
        初期化
        
        Args:
            parent: 親ウィジェット
        """
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        
        # UIの初期化
        self.init_ui()
        self.logger.info("UI initialized")
        
        # シグナルの接続
        self._connect_signals()
        self.logger.info("Signals connected")

    def init_ui(self):
        """UIを初期化する"""
        pass

    def _connect_signals(self):
        """シグナルを接続する"""
        pass

    def _disconnect_signals(self):
        """シグナルの接続を解除する"""
        pass

    def closeEvent(self, event):
        """
        ウィジェットが閉じられる時のイベント
        
        Args:
            event: クローズイベント
        """
        self._disconnect_signals()
        super().closeEvent(event)
