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
            self.logger.info("アプリケーションを起動しました")
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
                
            self.logger.debug(f"Loaded {len(groups)} groups")
                
        except Exception as e:
            self.logger.error(f"Error in load_data: {e}", exc_info=True)
            raise

    def on_group_changed(self, index):
        """グループ選択時の処理"""
        try:
            if index >= 0:
                group_id = self.group_combo.itemData(index)
                self.load_users(group_id)
                self.logger.debug(f"Group changed to index {index}, id {group_id}")
        except Exception as e:
            self.logger.error(f"Error in on_group_changed: {e}", exc_info=True)

    def load_users(self, group_id):
        """ユーザーリストの読み込み"""
        try:
            self.user_list.clear()
            users = self.db.get_users_by_group(group_id)
            
            for user in users:
                item = QListWidgetItem(user[1])
                item.setData(Qt.ItemDataRole.UserRole, user[0])
                self.user_list.addItem(item)
                
            self.logger.debug(f"Loaded {len(users)} users for group {group_id}")
        except Exception as e:
            self.logger.error(f"Error in load_users: {e}", exc_info=True)

    def on_user_selected(self):
        """ユーザー選択時の処理"""
        try:
            selected_items = self.user_list.selectedItems()
            if selected_items:
                user_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
                self.update_user_skills(user_id)
                self.logger.debug(f"User selected: {user_id}")
        except Exception as e:
            self.logger.error(f"Error in on_user_selected: {e}", exc_info=True)

    def update_user_skills(self, user_id):
        """ユーザーのスキルレベル表示を更新"""
        try:
            # TODO: スキルレベルの更新処理を実装
            self.logger.debug(f"Updating skills for user {user_id}")
            pass
        except Exception as e:
            self.logger.error(f"Error in update_user_skills: {e}", exc_info=True)

    def add_user(self):
        """ユーザーの追加"""
        try:
            if self.group_combo.currentIndex() < 0:
                QMessageBox.warning(self, "警告", "グループを選択してください")
                return
                
            name, ok = QInputDialog.getText(self, "ユーザー追加", "ユーザー名を入力:")
            if ok and name:
                group_id = self.group_combo.currentData()
                try:
                    self.db.add_user(name, group_id)
                    self.logger.debug(f"Adding user {name} to group {group_id}")
                    self.load_users(group_id)
                except Exception as e:
                    self.logger.error(f"Database error while adding user: {e}")
                    QMessageBox.critical(self, "エラー", "ユーザーの追加に失敗しました")
        except Exception as e:
            self.logger.error(f"Error in add_user: {e}", exc_info=True)

    def edit_user(self):
        """ユーザーの編集"""
        try:
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
                try:
                    if self.db.edit_user(user_id, new_name):
                        self.logger.debug(f"Editing user {user_id} name to {new_name}")
                        self.load_users(group_id)
                    else:
                        raise Exception("User not found")
                except Exception as e:
                    self.logger.error(f"Database error while editing user: {e}")
                    QMessageBox.critical(self, "エラー", "ユーザーの編集に失敗しました")
        except Exception as e:
            self.logger.error(f"Error in edit_user: {e}", exc_info=True)

    def delete_user(self):
        """ユーザーの削除"""
        try:
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
                
                # ユーザーの存在確認
                user = self.db.get_user(user_id)
                if not user:
                    QMessageBox.warning(self, "警告", "ユーザーが見つかりません")
                    return
                
                try:
                    if self.db.delete_user(user_id):
                        self.logger.debug(f"Deleting user {user_id}")
                        self.load_users(group_id)
                        QMessageBox.information(self, "完了", "ユーザーを削除しました")
                    else:
                        QMessageBox.warning(self, "警告", "ユーザーの削除に失敗しました")
                except Exception as e:
                    self.logger.error(f"Database error while deleting user: {e}")
                    QMessageBox.critical(self, "エラー", "ユーザーの削除に失敗しました")
        except Exception as e:
            self.logger.error(f"Error in delete_user: {e}", exc_info=True)

    def closeEvent(self, event):
        """アプリケーション終了時の処理"""
        try:
            self.logger.info("Application closing")
            self.window_closed.emit()
            event.accept()
        except Exception as e:
            self.logger.error(f"Error during closeEvent: {e}", exc_info=True)
            event.accept()
