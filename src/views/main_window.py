from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QListWidget,
    QTabWidget,
    QLabel,
    QSplitter,
    QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from .tabs.system_management.initial_settings_tab import InitialSettingsTab
from .tabs.system_management.data_io_tab import DataIOTab
from .tabs.system_management.system_info_tab import SystemInfoTab
from .tabs.category.category_tab import CategoryTab
from .tabs.evaluation.total_evaluation_tab import TotalEvaluationTab
from ..database.database_manager import DatabaseManager
from ..utils.time_utils import TimeProvider

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("スキルマトリックス管理システム")
        self.resize(1200, 800)

        # メインウィジェット
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ヘッダー
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
                padding: 10px;
            }
            QLabel {
                color: #212529;
                font-size: 12px;
            }
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 5, 10, 5)

        time_label = QLabel(f"Current Date and Time (UTC): {TimeProvider.get_formatted_time()}")
        user_label = QLabel(f"Current User's Login: {TimeProvider.get_current_user()}")
        
        header_layout.addWidget(time_label)
        header_layout.addStretch()
        header_layout.addWidget(user_label)
        
        main_layout.addWidget(header)

        # コンテンツ領域
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(content_widget)

        # スプリッター（3:7の分割）
        splitter = QSplitter(Qt.Orientation.Horizontal)
        content_layout.addWidget(splitter)

        # 左パネル（3）
        left_panel = QFrame()
        left_panel.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)

        # グループ選択
        group_frame = QFrame()
        group_layout = QVBoxLayout(group_frame)
        group_layout.setContentsMargins(0, 0, 0, 10)
        
        group_label = QLabel("グループ:")
        group_label.setFont(QFont("", 10, QFont.Weight.Bold))
        self.group_combo = QComboBox()
        self.group_combo.setMinimumHeight(30)
        
        group_layout.addWidget(group_label)
        group_layout.addWidget(self.group_combo)
        left_layout.addWidget(group_frame)

        # ユーザーリスト
        user_frame = QFrame()
        user_layout = QVBoxLayout(user_frame)
        user_layout.setContentsMargins(0, 0, 0, 10)
        
        user_label = QLabel("ユーザー一覧:")
        user_label.setFont(QFont("", 10, QFont.Weight.Bold))
        self.user_list = QListWidget()
        
        user_layout.addWidget(user_label)
        user_layout.addWidget(self.user_list)
        left_layout.addWidget(user_frame)

        # ボタングループ
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(5)

        self.add_user_btn = QPushButton("追加")
        self.edit_user_btn = QPushButton("編集")
        self.delete_user_btn = QPushButton("削除")

        for btn in [self.add_user_btn, self.edit_user_btn, self.delete_user_btn]:
            btn.setMinimumHeight(30)
            button_layout.addWidget(btn)

        left_layout.addWidget(button_frame)
        splitter.addWidget(left_panel)

        # 右パネル（7）
        right_panel = QFrame()
        right_panel.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)

        # タブウィジェット
        self.tab_widget = QTabWidget()
        right_layout.addWidget(self.tab_widget)

        # システム管理タブ
        system_tabs = QTabWidget()
        self.system_tab = InitialSettingsTab(self)
        self.data_io_tab = DataIOTab(self)
        self.system_info_tab = SystemInfoTab(self)

        system_tabs.addTab(self.system_tab, "初期設定")
        system_tabs.addTab(self.data_io_tab, "データ入出力")
        system_tabs.addTab(self.system_info_tab, "システム情報")

        self.tab_widget.addTab(system_tabs, "システム管理")
        
        # 総合評価タブ
        self.total_evaluation_tab = TotalEvaluationTab(self)
        self.tab_widget.addTab(self.total_evaluation_tab, "総合評価")

        splitter.addWidget(right_panel)
        
        # スプリッターの比率設定
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 7)

        self.apply_styles()
        self.load_initial_data()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QFrame {
                background-color: #ffffff;
            }
            QListWidget {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
            QComboBox {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 5px;
                background-color: #ffffff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(assets/down-arrow.png);
                width: 12px;
                height: 12px;
            }
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                border-bottom-color: #ffffff;
            }
            QLabel {
                color: #212529;
            }
        """)

    def load_initial_data(self):
        """初期データのロード"""
        groups = self.db.get_all_groups()
        self.group_combo.clear()
        for group in groups:
            self.group_combo.addItem(group[1], group[0])

        # ボタンの初期状態
        self.edit_user_btn.setEnabled(False)
        self.delete_user_btn.setEnabled(False)

    def add_category_tab(self, category_name):
        """カテゴリータブの追加"""
        new_tab = CategoryTab(self, category_name)
        index = self.tab_widget.count() - 2
        self.tab_widget.insertTab(index, new_tab, category_name)
        self.tab_widget.setCurrentIndex(index)
