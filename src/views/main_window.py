"""メインウィンドウモジュール"""
import logging
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QTabWidget,
    QComboBox, QMessageBox, QFrame, QSplitter,
    QGroupBox
)
from PyQt6.QtCore import Qt
from ..database.database_manager import DatabaseManager
from .system_management import SystemManagementWidget
from .category_management import CategoryWidget

class MainWindow(QMainWindow):
    """メインウィンドウクラス"""
    
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._db_manager = db_manager
        self._init_ui()

    def _init_ui(self):
        """UIの初期化"""
        self.setWindowTitle("スキルマトリックス管理")
        self.setMinimumSize(1200, 800)

        # メインウィジェット
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # メインレイアウト
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # 3:7のスプリッター
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左ペイン (3)
        left_pane = self._create_left_pane()
        splitter.addWidget(left_pane)
        
        # 右ペイン (7)
        right_pane = self._create_right_pane()
        splitter.addWidget(right_pane)
        
        # スプリッター比率設定
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 7)
        
        main_layout.addWidget(splitter)

    def _create_left_pane(self):
        """左ペインの作成 (グループ管理)"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # グループ選択
        group_box = QGroupBox("グループ選択")
        group_layout = QVBoxLayout()
        
        self.group_combo = QComboBox()
        group_layout.addWidget(self.group_combo)
        
        # ユーザーリスト
        self.user_list = QListWidget()
        group_layout.addWidget(self.user_list)
        
        # 操作ボタン
        button_layout = QVBoxLayout()
        add_user_btn = QPushButton("追加")
        edit_user_btn = QPushButton("編集")
        delete_user_btn = QPushButton("削除")
        
        button_layout.addWidget(add_user_btn)
        button_layout.addWidget(edit_user_btn)
        button_layout.addWidget(delete_user_btn)
        
        group_layout.addLayout(button_layout)
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        
        widget.setLayout(layout)
        return widget

    def _create_right_pane(self):
        """右ペインの作成 (タブ管理)"""
        self.tab_widget = QTabWidget()
        
        # システム管理タブ (デフォルト)
        system_tab = SystemManagementWidget(self._db_manager)
        self.tab_widget.addTab(system_tab, "システム管理")
        
        # 総合評価タブ
        evaluation_tab = CategoryWidget(self._db_manager, "総合評価")
        self.tab_widget.addTab(evaluation_tab, "総合評価")
        
        return self.tab_widget

    def add_category_tab(self, name: str):
        """カテゴリータブの追加"""
        new_tab = CategoryWidget(self._db_manager, name)
        # システム管理タブの左に挿入
        self.tab_widget.insertTab(
            self.tab_widget.count() - 1,
            new_tab,
            name
        )

