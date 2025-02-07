from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QMessageBox
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
        self.logger.debug("MainWindow parent initialization complete")
        
        # クラッシュ時のスタックトレース出力を設定
        sys.excepthook = self._exception_hook
        
        # メモリ管理の追跡
        self._debug_refs = set()
        
        self._initialize_components()
        self._setup_ui()
        self._connect_signals()
        
        # 初期データ読み込み
        QTimer.singleShot(100, self._safe_initial_load)

    def _initialize_components(self):
        """コンポーネントの初期化"""
        self.logger.debug("Initializing components")
        try:
            self.db = DatabaseManager()
            self.data_handler = DataHandler(self.db, self)
            self.event_handler = EventHandler(self.db, self)
            self.left_pane = LeftPane(self)
            self.right_pane = RightPane(self)
            
            # コンポーネントの参照を追跡
            for component in [self.data_handler, self.event_handler, self.left_pane, self.right_pane]:
                self._track_ref(component)
                
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
            
            self._track_ref(central_widget)
            self._track_ref(layout)
            
        except Exception as e:
            self.logger.critical(f"Failed to setup UI: {e}\n{traceback.format_exc()}")
            raise

    def _connect_signals(self):
        """シグナルの接続"""
        self.logger.debug("Connecting signals")
        try:
            # グループ変更
            self.left_pane.group_changed.connect(self.event_handler.on_group_changed)
            
            # ユーザー操作
            self.left_pane.add_user_clicked.connect(self.event_handler.add_user)
            self.left_pane.edit_user_clicked.connect(self.event_handler.edit_user)
            self.left_pane.delete_user_clicked.connect(self.event_handler.delete_user)
            
            # データ更新
            self.data_changed.connect(self.data_handler.refresh_data)
            
            self.logger.debug("Signal connections completed")
            
        except Exception as e:
            self.logger.error(f"Failed to connect signals: {e}\n{traceback.format_exc()}")

    def _safe_initial_load(self):
        """安全な初期データ読み込み"""
        self.logger.debug("Starting safe initial load")
        try:
            self.data_handler.load_initial_data()
        except Exception as e:
            self.logger.error(f"Error in initial load: {e}\n{traceback.format_exc()}")
            QMessageBox.critical(self, "エラー", "初期データの読み込みに失敗しました")

    def _track_ref(self, obj):
        """オブジェクト参照の追跡"""
        self._debug_refs.add(obj)
        self.logger.debug(f"Tracking new object: {obj.__class__.__name__}")

    def _exception_hook(self, exc_type, exc_value, exc_traceback):
        """未捕捉の例外をログに記録"""
        self.logger.critical(
            "Uncaught exception:",
            exc_info=(exc_type, exc_value, exc_traceback)
        )

    def closeEvent(self, event):
        """ウィンドウを閉じる際の処理"""
        self.logger.debug("Processing window close event")
        try:
            # クリーンアップ
            self._cleanup()
            self.window_closed.emit()
            self.logger.debug("Window closed signal emitted")
        except Exception as e:
            self.logger.error(f"Error in close event: {e}\n{traceback.format_exc()}")
        finally:
            event.accept()

    def _cleanup(self):
        """リソースのクリーンアップ"""
        self.logger.debug("Starting cleanup")
        try:
            # データハンドラーのクリーンアップ
            if hasattr(self, 'data_handler'):
                self.data_handler.cleanup()
            
            # イベントハンドラーのクリーンアップ
            if hasattr(self, 'event_handler'):
                self.event_handler.cleanup()
            
            # 参照の解放
            self._debug_refs.clear()
            
            self.logger.debug("Cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}\n{traceback.format_exc()}")
