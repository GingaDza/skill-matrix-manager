from PyQt6.QtWidgets import QMessageBox, QInputDialog, QDialog
from PyQt6.QtCore import QObject, Qt
import logging
import traceback
from typing import Optional

class EventHandler(QObject):
    """イベント処理を管理するハンドラー"""
    def __init__(self, db, main_window):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.db = db
        # メインウィンドウを直接参照
        self._main_window = main_window

    def cleanup(self):
        """リソースのクリーンアップ"""
        self.logger.debug("Cleaning up EventHandler")
        try:
            self._main_window = None
            self.db = None
        except Exception as e:
            self.logger.error(f"Error during EventHandler cleanup: {e}", exc_info=True)

    def _show_dialog(self, dialog_type: str, title: str, message: str,
                    default_text: str = "", buttons: QMessageBox.StandardButton = QMessageBox.StandardButton.Ok,
                    default_button: QMessageBox.StandardButton = QMessageBox.StandardButton.NoButton) -> tuple[Optional[str], bool]:
        """ダイアログを表示する汎用メソッド"""
        try:
            if dialog_type == "input":
                result = QInputDialog.getText(
                    self._main_window,
                    title,
                    message,
                    text=default_text
                )
                return result
            elif dialog_type == "question":
                result = QMessageBox.question(
                    self._main_window,
                    title,
                    message,
                    buttons,
                    default_button
                )
                return str(result), result == QMessageBox.StandardButton.Yes
            elif dialog_type == "error":
                QMessageBox.critical(
                    self._main_window,
                    title,
                    message
                )
                return None, False
            elif dialog_type == "warning":
                QMessageBox.warning(
                    self._main_window,
                    title,
                    message
                )
                return None, False
            elif dialog_type == "info":
                QMessageBox.information(
                    self._main_window,
                    title,
                    message
                )
                return None, False
        except Exception as e:
            self.logger.error(f"Dialog error: {e}", exc_info=True)
            return None, False

    def on_group_changed(self, index):
        """グループ変更時の処理"""
        self.logger.debug(f"Group changed to index {index}")
        if index >= 0 and self._main_window:
            try:
                self._main_window.data_handler.refresh_user_list()
            except Exception as e:
                self.logger.error(f"Error handling group change: {e}", exc_info=True)
                self._show_dialog("error", "エラー", "グループの変更中にエラーが発生しました")

    def add_user(self):
        """ユーザー追加"""
        self.logger.debug("Starting user addition")
        try:
            left_pane = self._main_window.left_pane
            group_id = left_pane.get_current_group_id()

            if group_id is None:
                self.logger.warning("No group selected for user addition")
                self._show_dialog("warning", "警告", "グループを選択してください")
                return

            name, ok = self._show_dialog(
                "input",
                "ユーザー追加",
                "ユーザー名を入力してください:"
            )

            if ok and name and name.strip():
                self.logger.debug(f"Adding user '{name}' to group {group_id}")
                if self.db.add_user(name.strip(), group_id):
                    self.logger.info(f"Successfully added user '{name}'")
                    self._main_window.data_changed.emit()
                    self._show_dialog(
                        "info",
                        "成功",
                        f"ユーザー '{name}' を追加しました"
                    )
                else:
                    self.logger.error("Failed to add user")
                    self._show_dialog(
                        "warning",
                        "警告",
                        "ユーザーの追加に失敗しました"
                    )

        except Exception as e:
            self.logger.error(f"Error adding user: {e}", exc_info=True)
            self._show_dialog(
                "error",
                "エラー",
                "ユーザーの追加中にエラーが発生しました"
            )

    def edit_user(self):
        """ユーザー編集"""
        self.logger.debug("Starting user edit")
        try:
            left_pane = self._main_window.left_pane
            current_item = left_pane.get_selected_user()

            if not current_item:
                self.logger.warning("No user selected for editing")
                self._show_dialog(
                    "warning",
                    "警告",
                    "編集するユーザーを選択してください"
                )
                return

            user_id = current_item.data(Qt.ItemDataRole.UserRole)
            current_name = current_item.text()

            new_name, ok = self._show_dialog(
                "input",
                "ユーザー編集",
                "新しいユーザー名を入力してください:",
                current_name
            )

            if ok and new_name and new_name.strip():
                self.logger.debug(f"Editing user {user_id} name to '{new_name}'")
                if self.db.edit_user(user_id, new_name.strip()):
                    self.logger.info(f"Successfully edited user {user_id}")
                    self._main_window.data_changed.emit()
                    self._show_dialog(
                        "info",
                        "成功",
                        f"ユーザー名を '{new_name}' に変更しました"
                    )
                else:
                    self.logger.error(f"Failed to edit user {user_id}")
                    self._show_dialog(
                        "warning",
                        "警告",
                        "ユーザーの編集に失敗しました"
                    )

        except Exception as e:
            self.logger.error(f"Error editing user: {e}", exc_info=True)
            self._show_dialog(
                "error",
                "エラー",
                "ユーザーの編集中にエラーが発生しました"
            )

    def delete_user(self):
        """ユーザー削除"""
        self.logger.debug("Starting user deletion")
        try:
            left_pane = self._main_window.left_pane
            current_item = left_pane.get_selected_user()

            if not current_item:
                self.logger.warning("No user selected for deletion")
                self._show_dialog(
                    "warning",
                    "警告",
                    "削除するユーザーを選択してください"
                )
                return

            user_id = current_item.data(Qt.ItemDataRole.UserRole)
            user_name = current_item.text()

            _, ok = self._show_dialog(
                "question",
                "確認",
                f"ユーザー '{user_name}' を削除してもよろしいですか？",
                buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                default_button=QMessageBox.StandardButton.No
            )

            if ok:
                self.logger.debug(f"Deleting user {user_id}")
                if self.db.delete_user(user_id):
                    self.logger.info(f"Successfully deleted user {user_id}")
                    self._main_window.user_deleted.emit(user_id)
                    self._main_window.data_changed.emit()
                    self._show_dialog(
                        "info",
                        "成功",
                        f"ユーザー '{user_name}' を削除しました"
                    )
                else:
                    self.logger.error(f"Failed to delete user {user_id}")
                    self._show_dialog(
                        "warning",
                        "警告",
                        "ユーザーの削除に失敗しました"
                    )

        except Exception as e:
            self.logger.error(f"Error deleting user: {e}", exc_info=True)
            self._show_dialog(
                "error",
                "エラー",
                "ユーザーの削除中にエラーが発生しました"
            )
