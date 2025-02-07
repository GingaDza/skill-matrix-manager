import logging
from PyQt6.QtWidgets import QMainWindow
from .views.main_window import MainWindow

class App(MainWindow):
    """アプリケーションのメインクラス"""
    def __init__(self):
        # 初期化の順序を修正
        QMainWindow.__init__(self)  # 最初にQMainWindowを初期化
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing App")
        self._setup_instance_variables()  # インスタンス変数の初期化
        self._setup_ui()  # UIの設定
        self._connect_signals()  # シグナルの接続
