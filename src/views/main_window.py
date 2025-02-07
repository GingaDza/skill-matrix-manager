from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QMessageBox,
    QInputDialog,
    QComboBox,
    QTabWidget,
    QSpinBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtCharts import QChart, QChartView, QPolarChart, QValueAxis
from ..database.database_manager import DatabaseManager
from .tabs.system_management.system_management_tab import SystemManagementTab
from .tabs.evaluation.total_evaluation_tab import TotalEvaluationTab
import logging

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.db = DatabaseManager()
        self.setup_ui()

    def setup_ui(self):
        """UIの初期設定"""
        self.setWindowTitle("スキルマトリックス管理システム")
        self.setGeometry(100, 100, 1400, 800)

        # メインウィジェット
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # 左ペイン (3:7の分割)
        left_pane = self._create_left_pane()
        main_layout.addWidget(left_pane, stretch=3)

        # 右ペイン (タブウィジェット)
        self.tab_widget = self._create_right_pane()
        main_layout.addWidget(self.tab_widget, stretch=7)

        # データの読み込み
        self.load_data()

    def _create_left_pane(self):
        """左ペインの作成"""
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
        layout.addWidget(button_widget)

        return widget

    def _create_right_pane(self):
        """右ペインの作成（タブウィジェット）"""
        tab_widget = QTabWidget()
        tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        tab_widget.setMovable(True)

        # システム管理タブ（デフォルト）
        self.system_tab = SystemManagementTab(self)
        tab_widget.addTab(self.system_tab, "システム管理")

        # 総合評価タブ
        self.evaluation_tab = TotalEvaluationTab(self)
        tab_widget.addTab(self.evaluation_tab, "総合評価")

        return tab_widget

    def load_data(self):
        """データの読み込み"""
        # グループの読み込み
        self.group_combo.clear()
        groups = self.db.get_all_groups()
        
        for group in groups:
            self.group_combo.addItem(group[1], group[0])

    def on_group_changed(self, index):
        """グループ選択時の処理"""
        if index >= 0:
            group_id = self.group_combo.itemData(index)
            self.load_users(group_id)

    def load_users(self, group_id):
        """ユーザーリストの読み込み"""
        self.user_list.clear()
        users = self.db.get_users_by_group(group_id)
        for user in users:
            item = QListWidgetItem(user[1])
            item.setData(Qt.ItemDataRole.UserRole, user[0])
            self.user_list.addItem(item)

    def on_user_selected(self):
        """ユーザー選択時の処理"""
        selected_items = self.user_list.selectedItems()
        if selected_items:
            self.update_user_skills(selected_items[0].data(Qt.ItemDataRole.UserRole))

    def update_user_skills(self, user_id):
        """ユーザーのスキルレベル表示を更新"""
        # 実装予定
        pass

    def add_user(self):
        """ユーザーの追加"""
        if self.group_combo.currentIndex() < 0:
            QMessageBox.warning(self, "警告", "グループを選択してください")
            return
            
        name, ok = QInputDialog.getText(self, "ユーザー追加", "ユーザー名を入力:")
        if ok and name:
            group_id = self.group_combo.currentData()
            # ユーザー追加の処理を実装予定
            self.load_users(group_id)

    def edit_user(self):
        """ユーザーの編集"""
        selected_items = self.user_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "ユーザーを選択してください")
            return
            
        current_name = selected_items[0].text()
        new_name, ok = QInputDialog.getText(
            self, "ユーザー編集", 
            "ユーザー名を入力:", 
            text=current_name
        )
        
        if ok and new_name:
            user_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
            group_id = self.group_combo.currentData()
            # ユーザー編集の処理を実装予定
            self.load_users(group_id)

    def delete_user(self):
        """ユーザーの削除"""
        selected_items = self.user_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "ユーザーを選択してください")
            return
            
        reply = QMessageBox.question(
            self, "確認", 
            "選択したユーザーを削除しますか？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            user_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
            group_id = self.group_combo.currentData()
            # ユーザー削除の処理を実装予定
            self.load_users(group_id)

    def closeEvent(self, event):
        """アプリケーション終了時の処理"""
        self.logger.info("アプリケーションを終了します")
        event.accept()
