from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QLabel,
    QMessageBox, QInputDialog, QComboBox, QTabWidget,
    QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter
from ..database.database_manager import DatabaseManager
from .tabs.system_management.system_management_tab import SystemManagementTab
from .tabs.evaluation.total_evaluation_tab import TotalEvaluationTab
import logging

class MainWindow(QMainWindow):
    """メインウィンドウクラス"""
    window_closed = pyqtSignal()
    user_deleted = pyqtSignal(int)  # ユーザー削除シグナル

    def __init__(self):
        """初期化"""
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug("MainWindow initialization started")
        
        try:
            self._setup_instance_variables()  # インスタンス変数の初期化
            self._setup_ui()  # UIの初期設定
            self._connect_signals()  # シグナルの接続
            self.logger.info("アプリケーションを起動しました")
        except Exception as e:
            self.logger.error(f"Error during MainWindow initialization: {e}", exc_info=True)
            raise

    # ... [残りのコードは同じ] ...
