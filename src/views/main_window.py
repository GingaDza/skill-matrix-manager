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
from ..utils.time_utils import TimeProvider

class MainWindow(QMainWindow):
    """アプリケーションのメインウィンドウ"""

    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        TimeProvider.set_current_user("GingaDza")
        self.setup_ui()

    def setup_ui(self):
        """UIの設定"""
        self.setWindowTitle("スキルマトリックス管理システム")
        self.resize(1200, 800)

        # メインウィジェット
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # メインレイアウト
        layout = QHBoxLayout()
        main_widget.setLayout(layout)

        # スプリッター（3:7の分割）
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)

        # 左側パネル（3）
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)

        # グループ選択コンボボックス
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

        # ユーザー操作ボタン
        button_layout = QVBoxLayout()
        self.add_user_btn = QPushButton("ユーザー追加")
        self.edit_user_btn = QPushButton("ユーザー編集")
        self.delete_user_btn = QPushButton("ユーザー削除")
        
        self.add_user_btn.clicked.connect(self.add_user)
        self.edit_user_btn.clicked.connect(self.edit_user)
        self.delete_user_btn.clicked.connect(self.delete_user)

        button_layout.addWidget(self.add_user_btn)
        button_layout.addWidget(self.edit_user_btn)
        button_layout.addWidget(self.delete_user_btn)
        left_layout.addLayout(button_layout)

        # 右側パネル（7）
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)

        # タブウィジェット
        self.tab_widget = QTabWidget()
        self.tab_widget.setMovable(True)  # タブの移動を許可
        right_layout.addWidget(self.tab_widget)

        # システム管理タブの追加
        self.system_tab = InitialSettingsTab(self)
        self.data_io_tab = DataIOTab(self)
        self.system_info_tab = SystemInfoTab(self)

        system_tabs = QTabWidget()
        system_tabs.addTab(self.system_tab, "初期設定")
        system_tabs.addTab(self.data_io_tab, "データ入出力")
        system_tabs.addTab(self.system_info_tab, "システム情報")

        self.tab_widget.addTab(system_tabs, "システム管理")

        # 総合評価タブ
        self.total_evaluation_tab = TotalEvaluationTab(self)
        self.tab_widget.addTab(self.total_evaluation_tab, "総合評価")

        # スプリッターに追加
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 3)  # 左側の比率
        splitter.setStretchFactor(1, 7)  # 右側の比率

        # 初期データの読み込み
        self.load_initial_data()

    def load_initial_data(self):
        """初期データの読み込み"""
        # グループの読み込み
        groups = self.db.get_all_groups()
        self.group_combo.clear()
        for group in groups:
            self.group_combo.addItem(group[1], group[0])  # name, id

    def on_group_changed(self, index):
        """グループ選択時の処理"""
        if index >= 0:
            group_id = self.group_combo.currentData()
            self.load_users_for_group(group_id)

    def load_users_for_group(self, group_id):
        """グループのユーザー一覧を読み込み"""
        self.user_list.clear()
        # TODO: グループに所属するユーザーの取得と表示

    def on_user_selected(self):
        """ユーザー選択時の処理"""
        has_selection = bool(self.user_list.selectedItems())
        self.edit_user_btn.setEnabled(has_selection)
        self.delete_user_btn.setEnabled(has_selection)

    def add_user(self):
        """ユーザーの追加"""
        # TODO: ユーザー追加ダイアログの表示

    def edit_user(self):
        """ユーザーの編集"""
        # TODO: ユーザー編集ダイアログの表示

    def delete_user(self):
        """ユーザーの削除"""
        # TODO: ユーザー削除の確認と実行

    def add_category_tab(self, category_name):
        """カテゴリータブの追加"""
        new_tab = CategoryTab(self, category_name)
        index = self.tab_widget.count() - 2  # システム管理と総合評価の前
        self.tab_widget.insertTab(index, new_tab, category_name)
        self.tab_widget.setCurrentIndex(index)

    def closeEvent(self, event):
        """ウィンドウを閉じる際の処理"""
        reply = QMessageBox.question(
            self,
            '確認',
            'アプリケーションを終了しますか？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
