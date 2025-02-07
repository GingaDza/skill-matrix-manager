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
        
        # macOSでのIMKClientの問題を回避
        if sys.platform == 'darwin':
            self.setAttribute(Qt.AA_DontUseNativeMenuBar)
        
        # アプリケーション情報の設定
        self.setApplicationName("スキルマトリックス管理システム")
        self.setApplicationVersion("1.0.0")
        
        # メインウィンドウの作成と表示
        self.main_window = MainWindow()
        self.main_window.show()
