"""メインウィンドウモジュール"""
import logging
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from ..database.database_manager import DatabaseManager

class MainWindow(QMainWindow):
    """メインウィンドウクラス"""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        メインウィンドウの初期化
        
        Args:
            db_manager (DatabaseManager): データベース管理インスタンス
        """
        super().__init__()
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("メインウィンドウを初期化中...")
        
        # データベース管理インスタンスの保持
        self._db_manager = db_manager
        
        try:
            self._init_ui()
        except Exception as e:
            self.logger.exception("UI初期化エラー")
            raise

    def _init_ui(self):
        """UIの初期化"""
        try:
            # ウィンドウの基本設定
            self.setWindowTitle("スキルマトリックス管理")
            self.setMinimumSize(800, 600)
            
            # セントラルウィジェット
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # メインレイアウト
            main_layout = QVBoxLayout()
            central_widget.setLayout(main_layout)
            
            self.logger.info("メインウィンドウのUI初期化完了")
            
        except Exception as e:
            self.logger.exception("UIコンポーネントの初期化エラー")
            raise

    def closeEvent(self, event):
        """
        ウィンドウを閉じる際の処理
        
        Args:
            event: クローズイベント
        """
        try:
            # クリーンアップ処理
            self._cleanup()
            event.accept()
            
        except Exception as e:
            self.logger.exception("終了処理エラー")
            event.ignore()

    def _cleanup(self):
        """リソースのクリーンアップ"""
        try:
            # データベース参照のクリア
            self._db_manager = None
            
            self.logger.info("メインウィンドウのクリーンアップ完了")
            
        except Exception as e:
            self.logger.exception("クリーンアップエラー")
            raise
