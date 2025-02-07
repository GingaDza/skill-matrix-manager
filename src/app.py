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
        
        # High DPI サポート
        self.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
        self.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
        
        # IMKClientの問題を回避
        if sys.platform == 'darwin':
            self.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar)
        
        # メインウィンドウの作成と表示
        self.main_window = MainWindow()
        self.main_window.show()

