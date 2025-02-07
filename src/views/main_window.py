from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QLabel,
    QMessageBox, QInputDialog, QComboBox, QTabWidget,
    QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter
from PyQt6.QtCharts import QChart, QChartView, QPolarChart, QValueAxis
from ..database.database_manager import DatabaseManager
from .tabs.system_management.system_management_tab import SystemManagementTab
from .tabs.evaluation.total_evaluation_tab import TotalEvaluationTab
import logging

class MainWindow(QMainWindow):
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug("MainWindow initialization started")
        
        try:
            self.db = DatabaseManager()
            self.setup_ui()
            self.logger.debug("MainWindow initialization completed")
        except Exception as e:
            self.logger.error(f"Error during MainWindow initialization: {e}", exc_info=True)
            raise

    def setup_ui(self):
        """UIの初期設定"""
        try:
            self.logger.debug("Setting up UI components")
            self.setWindowTitle("スキルマトリックス管理システム")
            self.setGeometry(100, 100, 1400, 800)
            
            # ウィンドウフラグの設定
            self.setWindowFlags(
                Qt.WindowType.Window |
                Qt.WindowType.CustomizeWindowHint |
                Qt.WindowType.WindowCloseButtonHint |
                Qt.WindowType.WindowMinMaxButtonsHint
            )

            # メインウィジェット
            main_widget = QWidget()
            self.setCentralWidget(main_widget)
            main_layout = QHBoxLayout(main_widget)

            # 左ペイン (3:7の分割)
            self.logger.debug("Creating left pane")
            left_pane = self._create_left_pane()
            main_layout.addWidget(left_pane, stretch=3)

            # 右ペイン (タブウィジェット)
            self.logger.debug("Creating right pane")
            self.tab_widget = self._create_right_pane()
            main_layout.addWidget(self.tab_widget, stretch=7)

            # データの読み込み
            self.logger.debug("Loading initial data")
            self.load_data()
            
        except Exception as e:
            self.logger.error(f"Error in setup_ui: {e}", exc_info=True)
            raise

    # ... [その他のメソッドは同じ] ...

