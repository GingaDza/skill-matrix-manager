from PyQt6.QtWidgets import QMainWindow
from .views.main_window import MainWindow
import logging

class App(MainWindow):
    def __init__(self):
        # ロギングの設定
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing App")
        
        try:
            super().__init__()
            self.logger.info("アプリケーションを起動しました")
        except Exception as e:
            self.logger.error(f"Error initializing App: {e}", exc_info=True)
            raise

    def closeEvent(self, event):
        try:
            self.logger.info("アプリケーションを終了します")
            super().closeEvent(event)
        except Exception as e:
            self.logger.error(f"Error in closeEvent: {e}", exc_info=True)
            event.accept()
