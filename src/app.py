import logging
from PyQt6.QtWidgets import QMainWindow
from .views.main_window import MainWindow

class App(MainWindow):
    """アプリケーションのメインクラス"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing App")
        super().__init__()  # MainWindowの初期化
