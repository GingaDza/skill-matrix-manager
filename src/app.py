import sys
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from .views.main_window import MainWindow

def setup_application_attributes():
    """アプリケーション属性の初期設定"""
    if sys.platform == 'darwin':
        # macOS特有の設定をアプリケーション作成前に適用
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_PluginApplication)
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar)
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontShowIconsInMenus)

class App(QApplication):
    """アプリケーションのメインクラス"""
    def __init__(self, argv):
        # アプリケーション作成前に属性を設定
        setup_application_attributes()
        
        super().__init__(argv)
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing App")
        
        # アプリケーション情報
        self.setApplicationName("スキルマトリックス管理システム")
        self.setApplicationVersion("1.0.0")
        self.setStyle("Fusion")  # プラットフォーム共通のスタイル
        
        # メインウィンドウ
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
