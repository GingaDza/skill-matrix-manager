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
from .tabs.system_management.initial_settings_tab import InitialSettingsTab
from .tabs.system_management.data_io_tab import DataIOTab
from .tabs.system_management.system_info_tab import SystemInfoTab
from .tabs.category.category_tab import CategoryTab
from .tabs.evaluation.total_evaluation_tab import TotalEvaluationTab
from ..database.database_manager import DatabaseManager

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

        # スプリッター（3:7の分割）
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左パネル（3）
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # グループ選択
        group_layout = QHBoxLayout()
        group_layout.addWidget(QLabel("グループ:"))
        self.group_combo = QComboBox()
        self.group_combo.currentIndexChanged.connect(self.on_group_changed)
        group_layout.addWidget(self.group_combo)
        left_layout.addLayout(group_layout)

        # ユーザーリスト
        self.user_list = QListWidget()
        self.user_list.itemSelectionChanged.connect(self.on_user_selected)
        left_layout.addWidget(self.user_list)

        # ボタン群
        button_layout = QVBoxLayout()
        self.add_user_btn = QPushButton("追加")
        self.edit_user_btn = QPushButton("編集")
        self.delete_user_btn = QPushButton("削除")
        
        # ボタンの接続
        self.add_user_btn.clicked.connect(self.on_add_user)
        self.edit_user_btn.clicked.connect(self.on_edit_user)
        self.delete_user_btn.clicked.connect(self.on_delete_user)
        
        button_layout.addWidget(self.add_user_btn)
        button_layout.addWidget(self.edit_user_btn)
        button_layout.addWidget(self.delete_user_btn)
        left_layout.addLayout(button_layout)

        splitter.addWidget(left_panel)

        # 右パネル（7）
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

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

        main_layout.addWidget(splitter)
        
        # 初期データのロード
        self.load_initial_data()

    def on_group_changed(self, index):
        """グループ選択時の処理"""
        if index >= 0:
            group_id = self.group_combo.currentData()
            self.load_users_for_group(group_id)

    def load_users_for_group(self, group_id):
        """グループのユーザー一覧を読み込み"""
        self.user_list.clear()
        users = self.db.get_users_by_group(group_id)
        for user in users:
            self.user_list.addItem(user[1])  # user[1] は name

    def on_user_selected(self):
        """ユーザー選択時の処理"""
        selected_items = self.user_list.selectedItems()
        if selected_items:
            user_name = selected_items[0].text()
            self.update_category_tabs(user_name)

    def on_add_user(self):
        """ユーザー追加ダイアログを表示"""
        pass  # システム管理タブの初期設定で実装

    def on_edit_user(self):
        """ユーザー編集ダイアログを表示"""
        pass  # システム管理タブの初期設定で実装

    def on_delete_user(self):
        """ユーザー削除の確認と実行"""
        pass  # システム管理タブの初期設定で実装

    def update_category_tabs(self, user_name):
        """カテゴリータブの内容を更新"""
        for i in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(i)
            if isinstance(tab, CategoryTab):
                tab.update_user_data(user_name)

    def load_initial_data(self):
        """初期データのロード"""
        groups = self.db.get_all_groups()
        self.group_combo.clear()
        for group in groups:
            self.group_combo.addItem(group[1], group[0])

    def add_category_tab(self, category_name):
        """カテゴリータブの追加"""
        new_tab = CategoryTab(self, category_name)
        index = self.tab_widget.count() - 2
        self.tab_widget.insertTab(index, new_tab, category_name)
        self.tab_widget.setCurrentIndex(index)
