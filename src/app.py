import logging
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from .views.main_window import MainWindow

class App(QApplication):
    """アプリケーションのメインクラス"""
    def __init__(self, argv):
        super().__init__(argv)
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing App")
        
        # アプリケーション情報の設定
        self.setApplicationName("スキルマトリックス管理システム")
        self.setApplicationVersion("1.0.0")
        self.setStyle("Fusion")
        
        # メインウィンドウのインスタンス化
        self.main_window = None

    def start(self):
        """アプリケーションの起動"""
        try:
            self.logger.debug("Starting application main window")
            self.main_window = MainWindow()
            self.main_window.show()
            return self.exec()
        except Exception as e:
            self.logger.error(f"Error starting application: {e}", exc_info=True)
            return 1
