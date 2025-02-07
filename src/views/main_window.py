from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QLabel,
    QMessageBox, QInputDialog, QComboBox, QTabWidget,
    QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter
from ..database.database_manager import DatabaseManager
from .tabs.system_management.system_management_tab import SystemManagementTab
from .tabs.evaluation.total_evaluation_tab import TotalEvaluationTab
import logging

class MainWindow(QMainWindow):
    """メインウィンドウクラス"""
    window_closed = pyqtSignal()
    user_deleted = pyqtSignal(int)  # ユーザー削除シグナル

    def __init__(self):
        """初期化"""
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug("MainWindow initialization started")
        
        try:
            self._setup_instance_variables()
            self.setup_ui()
            self._connect_signals()
            self.logger.info("アプリケーションを起動しました")
        except Exception as e:
            self.logger.error(f"Error during MainWindow initialization: {e}", exc_info=True)
            raise

    def _setup_instance_variables(self):
        """インスタンス変数の初期化"""
        self.db = DatabaseManager()
        self.current_user_id = None
        self.current_group_id = None

    def _connect_signals(self):
        """シグナルの接続"""
        try:
            self.user_deleted.connect(self._on_user_deleted)
        except Exception as e:
            self.logger.error(f"Error connecting signals: {e}", exc_info=True)
            raise

    def _on_user_deleted(self, user_id):
        """ユーザー削除後の処理"""
        try:
            if self.current_user_id == user_id:
                self.current_user_id = None
            if self.current_group_id:
                self.load_users(self.current_group_id)
        except Exception as e:
            self.logger.error(f"Error in _on_user_deleted: {e}", exc_info=True)

    def delete_user(self):
        """ユーザーの削除"""
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
                try:
                    if self.db.delete_user(user_id):
                        self.logger.info(f"User {user_id} ({user_name}) deleted successfully")
                        self.user_list.takeItem(self.user_list.row(current_item))
                        
                        if self.current_user_id == user_id:
                            self.current_user_id = None
                            
                        self.user_deleted.emit(user_id)
                        QMessageBox.information(self, "完了", f"ユーザー「{user_name}」を削除しました")
                    else:
                        QMessageBox.warning(self, "警告", "ユーザーの削除に失敗しました")
                except Exception as e:
                    self.logger.error(f"Database error while deleting user: {e}", exc_info=True)
                    QMessageBox.critical(self, "エラー", "データベースエラーが発生しました")

        except Exception as e:
            self.logger.error(f"Error in delete_user: {e}", exc_info=True)
            QMessageBox.critical(self, "エラー", "予期せぬエラーが発生しました")

    def on_user_selected(self):
        """ユーザー選択時の処理"""
        try:
            selected_items = self.user_list.selectedItems()
            if selected_items:
                user_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
                self.current_user_id = user_id
                self.update_user_skills(user_id)
                self.logger.debug(f"User selected: {user_id}")
        except Exception as e:
            self.logger.error(f"Error in on_user_selected: {e}", exc_info=True)

    def on_group_changed(self, index):
        """グループ選択時の処理"""
        try:
            if index >= 0:
                group_id = self.group_combo.itemData(index)
                self.current_group_id = group_id
                self.load_users(group_id)
                self.logger.debug(f"Group changed to index {index}, id {group_id}")
        except Exception as e:
            self.logger.error(f"Error in on_group_changed: {e}", exc_info=True)

    # ... [他のメソッドは同じ] ...
