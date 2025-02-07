import logging
from PyQt6.QtWidgets import QMainWindow
from .views.main_window import MainWindow

class App(MainWindow):
    """アプリケーションのメインクラス"""
    def __init__(self):
        super().__init__()  # 親クラスの初期化
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing App")
        self.show()  # ウィンドウを表示
