from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
import logging
from typing import Optional
from ..database.database_manager import DatabaseManager
from .components.left_pane import LeftPane
from .components.right_pane import RightPane
from .handlers.memory_optimized_handler import MemoryOptimizedHandler as DataHandler
from .handlers.event_handler import EventHandler

class MainWindow(QMainWindow):
    """メインウィンドウクラス"""
    
    # カスタムシグナル
    window_closed = pyqtSignal()  # ウィンドウが閉じられた時のシグナル
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Starting MainWindow initialization")
        
        super().__init__()
        self.logger.debug("MainWindow parent initialization complete")
        
        # コンポーネントの初期化
        self.logger.debug("Initializing components")
        try:
            self._initialize_components()
        except Exception as e:
            self.logger.critical(f"Failed to initialize components: {e}")
            raise
            
        # UIのセットアップ
        self.logger.debug("Setting up UI")
        try:
            self._setup_ui()
        except Exception as e:
            self.logger.critical(f"Failed to setup UI: {e}")
            raise
            
        # シグナルの接続
        self.logger.debug("Connecting signals")
        try:
            self._connect_signals()
        except Exception as e:
            self.logger.critical(f"Failed to connect signals: {e}")
            raise
            
        self.logger.debug("Signal connections completed")
        
        # 初期データの安全な読み込み
        self.logger.debug("Starting safe initial load")
        try:
            self._safe_initial_load()
        except Exception as e:
            self.logger.critical(f"Failed to load initial data: {e}")
            raise

    def _initialize_components(self):
        """コンポーネントの初期化"""
        # データベースの初期化
        self.db = DatabaseManager()
        
        # 左ペインの初期化
        self.left_pane = LeftPane()
        self.logger.debug("Tracking new object: LeftPane")
        
        # 右ペインの初期化
        self.right_pane = RightPane()
        self.logger.debug("Tracking new object: RightPane")
        
        # データハンドラーの初期化
        self.data_handler = DataHandler(self.db, self)
        self.logger.debug("Tracking new object: MemoryOptimizedHandler")
        
        # イベントハンドラーの初期化
        self.event_handler = EventHandler(self.db, self, self.data_handler)
        self.logger.debug("Tracking new object: EventHandler")

    def _setup_ui(self):
        """UIのセットアップ"""
        # メインウィジェットの設定
        main_widget = QWidget()
        self.logger.debug("Tracking new object: QWidget")
        
        # レイアウトの設定
        layout = QHBoxLayout()
        self.logger.debug("Tracking new object: QHBoxLayout")
        
        # ウィジェットの配置
        layout.addWidget(self.left_pane)
        layout.addWidget(self.right_pane)
        
        # レイアウトの適用
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        
        # ウィンドウの設定
        self.setWindowTitle("スキルマトリクス管理")
        self.setGeometry(100, 100, 800, 600)

    def _connect_signals(self):
        """シグナルの接続"""
        # 左ペインのシグナル接続
        self.left_pane.connect_signals(self.event_handler)
        
        # 右ペインのシグナル接続
        self.right_pane.connect_signals(self.event_handler)

    def _safe_initial_load(self):
        """初期データの安全な読み込み"""
        try:
            self.data_handler.load_initial_data()
        except Exception as e:
            self.logger.error(f"初期データ読み込みエラー: {e}")
            raise

    def closeEvent(self, event):
        """終了時の処理"""
        try:
            self.logger.info("ウィンドウのクローズイベントを処理")
            
            # データハンドラーのクリーンアップ
            if hasattr(self, 'data_handler'):
                self.data_handler.cleanup()
            
            # イベントハンドラーのクリーンアップ
            if hasattr(self, 'event_handler'):
                self.event_handler.cleanup()
                
            # 閉じるシグナルの発行
            self.window_closed.emit()
            
            # 基底クラスの処理
            super().closeEvent(event)
            
            self.logger.info("ウィンドウの終了処理が完了")
            
        except Exception as e:
            self.logger.error(f"終了処理エラー: {e}")
            event.accept()
