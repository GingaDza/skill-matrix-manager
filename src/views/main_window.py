from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QComboBox, QLabel, QPushButton,
    QListWidget, QTabWidget, QStatusBar
)
from PyQt6.QtCore import Qt, pyqtSignal
import logging
from datetime import datetime

from .tabs.system_management.initial_settings_tab import InitialSettingsTab
from .tabs.system_management.data_io_tab import DataIOTab
from .tabs.system_management.system_info_tab import SystemInfoTab
from .components.lists.group_list_widget import GroupListWidget
from ..database.database_manager import DatabaseManager

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.setup_ui()
        logger.debug("MainWindow initialized")

    def setup_ui(self):
        self.setWindowTitle("スキルマトリックス管理システム")
        self.setMinimumSize(1200, 800)

        # メインウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # メインスプリッター (3:7の分割)
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setStretchFactor(0, 3)
        main_splitter.setStretchFactor(1, 7)

        # 左側のウィジェット
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # グループ選択コンボボックス
        group_section = QWidget()
        group_layout = QHBoxLayout(group_section)
        group_layout.addWidget(QLabel("グループ:"))
        self.group_combo = QComboBox()
        group_layout.addWidget(self.group_combo)
        left_layout.addWidget(group_section)

        # ユーザーリスト
        self.user_list = QListWidget()
        left_layout.addWidget(self.user_list)

        # ユーザー操作ボタン
        button_layout = QHBoxLayout()
        add_user_btn = QPushButton("追加")
        edit_user_btn = QPushButton("編集")
        delete_user_btn = QPushButton("削除")

        button_layout.addWidget(add_user_btn)
        button_layout.addWidget(edit_user_btn)
        button_layout.addWidget(delete_user_btn)
        left_layout.addLayout(button_layout)

        # 右側のタブウィジェット
        self.tab_widget = QTabWidget()
        
        # システム管理タブ
        self.system_tab = InitialSettingsTab(self)
        self.data_io_tab = DataIOTab(self)
        self.system_info_tab = SystemInfoTab(self)
        
        # タブの追加
        self.tab_widget.addTab(self.system_tab, "システム管理")

        # スプリッターに追加
        main_splitter.addWidget(left_widget)
        main_splitter.addWidget(self.tab_widget)
        layout.addWidget(main_splitter)

        # ステータスバー
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status()

        logger.debug("MainWindow UI setup completed")

    def update_status(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_bar.showMessage(f"最終更新: {current_time}")
