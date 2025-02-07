from PyQt6.QtWidgets import QApplication
from .views.main_window import MainWindow
import logging

class App(MainWindow):
    def __init__(self):
        # ロギングの設定
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # メインウィンドウの初期化
        super().__init__()
        self.logger.info("アプリケーションを起動しました")

    def closeEvent(self, event):
        self.logger.info("アプリケーションを終了します")
        event.accept()
