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
    window_closed = pyqtSignal()  # ウィンドウクローズシグナル

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

    def _create_left_pane(self):
        """左ペインの作成"""
        try:
            self.logger.debug("Creating left pane components")
            widget = QWidget()
            layout = QVBoxLayout(widget)

            # グループ選択
            group_widget = QWidget()
            group_layout = QVBoxLayout(group_widget)
            group_layout.addWidget(QLabel("グループ選択"))
            self.group_combo = QComboBox()
            self.group_combo.currentIndexChanged.connect(self.on_group_changed)
            group_layout.addWidget(self.group_combo)
            layout.addWidget(group_widget)

            # ユーザーリスト
            user_widget = QWidget()
            user_layout = QVBoxLayout(user_widget)
            user_layout.addWidget(QLabel("ユーザーリスト"))
            self.user_list = QListWidget()
            self.user_list.itemSelectionChanged.connect(self.on_user_selected)
            user_layout.addWidget(self.user_list)
            layout.addWidget(user_widget)

            # ユーザー操作ボタン
            button_widget = self._create_user_buttons()
            layout.addWidget(button_widget)

            return widget
            
        except Exception as e:
            self.logger.error(f"Error in _create_left_pane: {e}", exc_info=True)
            raise

    def _create_user_buttons(self):
        """ユーザー操作ボタンの作成"""
        try:
            button_widget = QWidget()
            button_layout = QVBoxLayout(button_widget)
            
            self.add_user_btn = QPushButton("ユーザー追加")
            self.edit_user_btn = QPushButton("ユーザー編集")
            self.delete_user_btn = QPushButton("ユーザー削除")

            self.add_user_btn.clicked.connect(self.add_user)
            self.edit_user_btn.clicked.connect(self.edit_user)
            self.delete_user_btn.clicked.connect(self.delete_user)

            button_layout.addWidget(self.add_user_btn)
            button_layout.addWidget(self.edit_user_btn)
            button_layout.addWidget(self.delete_user_btn)

            return button_widget
            
        except Exception as e:
            self.logger.error(f"Error in _create_user_buttons: {e}", exc_info=True)
            raise

    def _create_right_pane(self):
        """右ペインの作成（タブウィジェット）"""
        try:
            self.logger.debug("Creating right pane with tabs")
            tab_widget = QTabWidget()
            tab_widget.setTabPosition(QTabWidget.TabPosition.North)
            tab_widget.setMovable(True)

            # システム管理タブ（デフォルト）
            self.logger.debug("Creating system management tab")
            self.system_tab = SystemManagementTab(self)
            tab_widget.addTab(self.system_tab, "システム管理")

            # 総合評価タブ
            self.logger.debug("Creating evaluation tab")
            self.evaluation_tab = TotalEvaluationTab(self)
            tab_widget.addTab(self.evaluation_tab, "総合評価")

            return tab_widget
            
        except Exception as e:
            self.logger.error(f"Error in _create_right_pane: {e}", exc_info=True)
            raise

    def load_data(self):
        """データの読み込み"""
        try:
            self.logger.debug("Loading group data")
            self.group_combo.clear()
            groups = self.db.get_all_groups()
            
            for group in groups:
                self.group_combo.addItem(group[1], group[0])
                
        except Exception as e:
            self.logger.error(f"Error in load_data: {e}", exc_info=True)
            raise

    def closeEvent(self, event):
        """アプリケーション終了時の処理"""
        try:
            self.logger.info("Application closing")
            self.window_closed.emit()
            event.accept()
        except Exception as e:
            self.logger.error(f"Error during closeEvent: {e}", exc_info=True)
            event.accept()

    # ... [その他のメソッドは同じ] ...

