import logging
from .views.main_window import MainWindow

class App(MainWindow):
    """アプリケーションメインクラス"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing App")
        super().__init__()  # MainWindowの初期化
