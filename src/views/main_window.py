from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QLabel,
    QMessageBox, QInputDialog, QComboBox, QTabWidget,
    QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from ..database.database_manager import DatabaseManager
from .tabs.system_management.system_management_tab import SystemManagementTab
from .tabs.evaluation.total_evaluation_tab import TotalEvaluationTab
import logging

class MainWindow(QMainWindow):
    """メインウィンドウクラス"""
    window_closed = pyqtSignal()
    user_deleted = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug("MainWindow initialization started")
        
        self._setup_instance_variables()
        self._setup_ui()
        self._connect_signals()

    def _setup_instance_variables(self):
        """インスタンス変数の初期化"""
        self.db = DatabaseManager()
        self.current_user_id = None
        self.current_group_id = None
        self.group_combo = None
        self.user_list = None
        self.system_tab = None
        self.evaluation_tab = None
        # 更新用タイマー
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self._delayed_update)

    def _setup_ui(self):
        """UIのセットアップ"""
        self.setWindowTitle("スキルマトリックス管理システム")
        self.setMinimumSize(800, 600)
        self.resize(1200, 800)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        left_pane = self._create_left_pane()
        right_pane = self._create_right_pane()
        
        main_layout.addWidget(left_pane, stretch=3)
        main_layout.addWidget(right_pane, stretch=7)
        
        self.load_data()

    def _create_left_pane(self):
        """左ペインの作成"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # グループ選択
        group_widget = QWidget()
        group_layout = QVBoxLayout(group_widget)
        group_label = QLabel("グループ選択")
        self.group_combo = QComboBox()
        self.group_combo.currentIndexChanged.connect(self._safe_on_group_changed)
        
        group_layout.addWidget(group_label)
        group_layout.addWidget(self.group_combo)
        layout.addWidget(group_widget)

        # ユーザーリスト
        user_widget = QWidget()
        user_layout = QVBoxLayout(user_widget)
        user_label = QLabel("ユーザーリスト")
        self.user_list = QListWidget()
        self.user_list.itemSelectionChanged.connect(self._safe_on_user_selected)
        
        user_layout.addWidget(user_label)
        user_layout.addWidget(self.user_list)
        layout.addWidget(user_widget)

        # ボタン
        button_widget = self._create_user_buttons()
        layout.addWidget(button_widget)

        return widget

    def _create_user_buttons(self):
        """ユーザー操作ボタンの作成"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        add_button = QPushButton("ユーザー追加")
        edit_button = QPushButton("ユーザー編集")
        delete_button = QPushButton("ユーザー削除")

        add_button.clicked.connect(self._safe_add_user)
        edit_button.clicked.connect(self._safe_edit_user)
        delete_button.clicked.connect(self._safe_delete_user)

        layout.addWidget(add_button)
        layout.addWidget(edit_button)
        layout.addWidget(delete_button)
        layout.addStretch()

        return widget

    def _create_right_pane(self):
        """右ペインの作成"""
        tab_widget = QTabWidget()
        
        self.system_tab = SystemManagementTab(self)
        self.evaluation_tab = TotalEvaluationTab(self)
        
        tab_widget.addTab(self.system_tab, "システム管理")
        tab_widget.addTab(self.evaluation_tab, "総合評価")

        return tab_widget

    def _connect_signals(self):
        """シグナルの接続"""
        self.user_deleted.connect(self._on_user_deleted)

    def _safe_on_group_changed(self, index):
        """グループ変更の安全な処理"""
        try:
            if index >= 0:
                group_id = self.group_combo.itemData(index)
                self.current_group_id = group_id
                self.load_users(group_id)
        except Exception as e:
            self.logger.error(f"Error in group change: {e}", exc_info=True)
            QMessageBox.critical(self, "エラー", "グループの変更中にエラーが発生しました")

    def _safe_on_user_selected(self):
        """ユーザー選択の安全な処理"""
        try:
            selected_items = self.user_list.selectedItems()
            if selected_items:
                user_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
                self.current_user_id = user_id
                self.update_user_skills(user_id)
        except Exception as e:
            self.logger.error(f"Error in user selection: {e}", exc_info=True)
            QMessageBox.critical(self, "エラー", "ユーザーの選択中にエラーが発生しました")

    def load_data(self):
        """データの読み込み"""
        try:
            groups = self.db.get_all_groups()
            self.group_combo.clear()
            
            for group in groups:
                self.group_combo.addItem(group[1], group[0])
        except Exception as e:
            self.logger.error(f"Error loading data: {e}", exc_info=True)
            QMessageBox.critical(self, "エラー", "データの読み込みに失敗しました")

    def load_users(self, group_id):
        """ユーザーリストの読み込み"""
        try:
            users = self.db.get_users_by_group(group_id)
            self.user_list.clear()
            
            for user in users:
                item = QListWidgetItem(user[1])
                item.setData(Qt.ItemDataRole.UserRole, user[0])
                self.user_list.addItem(item)
        except Exception as e:
            self.logger.error(f"Error loading users: {e}", exc_info=True)
            QMessageBox.critical(self, "エラー", "ユーザーリストの読み込みに失敗しました")

    def _delayed_update(self):
        """遅延更新の実行"""
        try:
            if self.current_group_id is not None:
                self.load_users(self.current_group_id)
        except Exception as e:
            self.logger.error(f"Error in delayed update: {e}", exc_info=True)

    def schedule_update(self):
        """更新のスケジュール"""
        self.update_timer.start(100)  # 100ms後に更新

    def _safe_add_user(self):
        """ユーザー追加の安全な処理"""
        try:
            if self.group_combo.currentIndex() < 0:
                QMessageBox.warning(self, "警告", "グループを選択してください")
                return

            name, ok = QInputDialog.getText(self, "ユーザー追加", "ユーザー名を入力:")
            if ok and name:
                group_id = self.group_combo.currentData()
                user_id = self.db.add_user(name, group_id)
                
                if user_id:
                    self.schedule_update()
                    QMessageBox.information(self, "完了", f"ユーザー「{name}」を追加しました")
                else:
                    QMessageBox.warning(self, "警告", "ユーザーの追加に失敗しました")
        except Exception as e:
            self.logger.error(f"Error adding user: {e}", exc_info=True)
            QMessageBox.critical(self, "エラー", "ユーザーの追加中にエラーが発生しました")

    def _safe_edit_user(self):
        """ユーザー編集の安全な処理"""
        try:
            selected_items = self.user_list.selectedItems()
            if not selected_items:
                QMessageBox.warning(self, "警告", "ユーザーを選択してください")
                return

            current_item = selected_items[0]
            user_id = current_item.data(Qt.ItemDataRole.UserRole)
            current_name = current_item.text()

            new_name, ok = QInputDialog.getText(
                self, "ユーザー編集", 
                "新しいユーザー名を入力:",
                text=current_name
            )

            if ok and new_name:
                if self.db.edit_user(user_id, new_name):
                    self.schedule_update()
                    QMessageBox.information(self, "完了", f"ユーザー名を「{new_name}」に変更しました")
                else:
                    QMessageBox.warning(self, "警告", "ユーザーの編集に失敗しました")
        except Exception as e:
            self.logger.error(f"Error editing user: {e}", exc_info=True)
            QMessageBox.critical(self, "エラー", "ユーザーの編集中にエラーが発生しました")

    def _safe_delete_user(self):
        """ユーザー削除の安全な処理"""
        try:
            selected_items = self.user_list.selectedItems()
            if not selected_items:
                QMessageBox.warning(self, "警告", "ユーザーを選択してください")
                return

            current_item = selected_items[0]
            user_id = current_item.data(Qt.ItemDataRole.UserRole)
            user_name = current_item.text()

            reply = QMessageBox.question(
                self,
                "確認",
                f"ユーザー「{user_name}」を削除してもよろしいですか？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                if self.db.delete_user(user_id):
                    self.user_list.takeItem(self.user_list.row(current_item))
                    if self.current_user_id == user_id:
                        self.current_user_id = None
                    self.user_deleted.emit(user_id)
                    self.schedule_update()
                    QMessageBox.information(self, "完了", f"ユーザー「{user_name}」を削除しました")
                else:
                    QMessageBox.warning(self, "警告", "ユーザーの削除に失敗しました")
        except Exception as e:
            self.logger.error(f"Error deleting user: {e}", exc_info=True)
            QMessageBox.critical(self, "エラー", "ユーザーの削除中にエラーが発生しました")

    def _on_user_deleted(self, user_id):
        """ユーザー削除後の処理"""
        try:
            if self.current_user_id == user_id:
                self.current_user_id = None
            if self.current_group_id:
                self.schedule_update()
        except Exception as e:
            self.logger.error(f"Error in user deletion callback: {e}", exc_info=True)

    def update_user_skills(self, user_id):
        """ユーザースキルの更新"""
        pass  # 実装予定

    def closeEvent(self, event):
        """ウィンドウ終了時の処理"""
        try:
            self.window_closed.emit()
            event.accept()
        except Exception as e:
            self.logger.error(f"Error in window close: {e}", exc_info=True)
            event.accept()
