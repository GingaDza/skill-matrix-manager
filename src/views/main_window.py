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
    QSplitter
)
from PyQt6.QtCore import Qt
from .components.header_widget import HeaderWidget
from .tabs.system_management.initial_settings_tab import InitialSettingsTab
from .tabs.system_management.data_io_tab import DataIOTab
from .tabs.system_management.system_info_tab import SystemInfoTab
from .tabs.category.category_tab import CategoryTab
from .tabs.evaluation.total_evaluation_tab import TotalEvaluationTab
from ..database.database_manager import DatabaseManager

class MainWindow(QMainWindow):
    """アプリケーションのメインウィンドウ"""

    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.setup_ui()

    def setup_ui(self):
        """UIの設定"""
        self.setWindowTitle("スキルマトリックス管理システム")
        self.resize(1200, 800)

        # メインウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # メインレイアウト
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # ヘッダーの追加
        header = HeaderWidget()
        main_layout.addWidget(header)

        # コンテンツ領域
        content_layout = QHBoxLayout()

        # スプリッター（3:7の分割）
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # 左パネル（3）
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)

        # グループ選択
        group_layout = QHBoxLayout()
        group_layout.addWidget(QLabel("グループ:"))
        self.group_combo = QComboBox()
        group_layout.addWidget(self.group_combo)
        left_layout.addLayout(group_layout)

        # ユーザーリスト
        self.user_list = QListWidget()
        left_layout.addWidget(self.user_list)

        # ボタン群
        button_layout = QVBoxLayout()
        self.add_user_btn = QPushButton("追加")
        self.edit_user_btn = QPushButton("編集")
        self.delete_user_btn = QPushButton("削除")
        
        button_layout.addWidget(self.add_user_btn)
        button_layout.addWidget(self.edit_user_btn)
        button_layout.addWidget(self.delete_user_btn)
        left_layout.addLayout(button_layout)

        # 右パネル（7）
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)

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

        # スプリッターにパネルを追加
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 7)

        content_layout.addWidget(splitter)
        main_layout.addLayout(content_layout)

        # スタイルの適用
        self.apply_styles()
        
        # 初期データのロード
        self.load_initial_data()

    def apply_styles(self):
        """スタイルの適用"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QSplitter {
                background-color: #ffffff;
            }
            QListWidget {
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QComboBox {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #f8f9fa;
                border: 1px solid #cccccc;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                border-bottom: none;
            }
        """)

    def load_initial_data(self):
        """初期データのロード"""
        # グループデータのロード
        groups = self.db.get_all_groups()
        self.group_combo.clear()
        for group in groups:
            self.group_combo.addItem(group[1], group[0])

    def add_category_tab(self, category_name):
        """カテゴリータブの追加"""
        new_tab = CategoryTab(self, category_name)
        index = self.tab_widget.count() - 2  # システム管理と総合評価の前
        self.tab_widget.insertTab(index, new_tab, category_name)
        self.tab_widget.setCurrentIndex(index)
