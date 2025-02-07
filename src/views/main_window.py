from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QCoreApplication
import logging
import sys
import traceback
from .components.left_pane import LeftPane
from .components.right_pane import RightPane
from .handlers.data_handler import DataHandler
from .handlers.event_handler import EventHandler
from ..database.database_manager import DatabaseManager

class MainWindow(QMainWindow):
    """メインウィンドウクラス"""
    window_closed = pyqtSignal()
    user_deleted = pyqtSignal(int)
    data_changed = pyqtSignal()

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("Starting MainWindow initialization")
        
        if not QCoreApplication.instance():
            self.logger.critical("QApplication not created before MainWindow")
            raise RuntimeError("QApplication must be created before MainWindow")
            
        super().__init__()
        
        # クラッシュ時のスタックトレース出力を設定
        sys.excepthook = self._exception_hook
        
        self._initialize_components()
        self._setup_ui()
        self._connect_signals()
        
        # 初期データ読み込み
        QTimer.singleShot(100, self.data_handler.load_initial_data)

    def _initialize_components(self):
        """コンポーネントの初期化"""
        self.logger.debug("Initializing components")
        try:
            self.db = DatabaseManager()
            self.data_handler = DataHandler(self.db, self)
            self.event_handler = EventHandler(self.db, self)
            self.left_pane = LeftPane(self)
            self.right_pane = RightPane(self)
        except Exception as e:
            self.logger.critical(f"Failed to initialize components: {e}\n{traceback.format_exc()}")
            raise

    def _setup_ui(self):
        """UIのセットアップ"""
        self.logger.debug("Setting up UI")
        try:
            self.setWindowTitle("スキルマトリックス管理システム")
            self.setMinimumSize(800, 600)
            
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            layout = QHBoxLayout(central_widget)
            layout.addWidget(self.left_pane, stretch=1)
            layout.addWidget(self.right_pane, stretch=2)
        except Exception as e:
            self.logger.critical(f"Failed to setup UI: {e}\n{traceback.format_exc()}")
            raise

    def _connect_signals(self):
        """シグナルの接続"""
        self.logger.debug("Connecting signals")
        try:
            self.left_pane.group_changed.connect(self.event_handler.on_group_changed)
            self.left_pane.add_user_clicked.connect(self.event_handler.add_user)
            self.left_pane.edit_user_clicked.connect(self.event_handler.edit_user)
            self.left_pane.delete_user_clicked.connect(self.event_handler.delete_user)
            self.data_changed.connect(self.data_handler.refresh_data)
        except Exception as e:
            self.logger.error(f"Failed to connect signals: {e}\n{traceback.format_exc()}")

    def _exception_hook(self, exc_type, exc_value, exc_traceback):
        """未捕捉の例外をログに記録"""
        self.logger.critical("Uncaught exception:",
                           exc_info=(exc_type, exc_value, exc_traceback))

    def closeEvent(self, event):
        """ウィンドウを閉じる際の処理"""
        self.logger.debug("Processing window close event")
        try:
            self.window_closed.emit()
            self.logger.debug("Window closed signal emitted")
        except Exception as e:
            self.logger.error(f"Error in close event: {e}\n{traceback.format_exc()}")
        finally:
            event.accept()
