from PyQt6.QtWidgets import QMessageBox, QInputDialog
from PyQt6.QtCore import QObject, Qt
import logging
import traceback
import weakref

class EventHandler(QObject):
    """イベント処理を管理するハンドラー"""
    def __init__(self, db, main_window):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.db = db
        # メインウィンドウへの弱参照を使用
        self._main_window = weakref.proxy(main_window)

    @property
    def main_window(self):
        """メインウィンドウへの安全なアクセス"""
        try:
            return self._main_window
        except ReferenceError:
            self.logger.error("Main window reference lost")
            return None

    def cleanup(self):
        """リソースのクリーンアップ"""
        self.logger.debug("Cleaning up EventHandler")
        try:
            # 参照のクリア
            self._main_window = None
            self.db = None
        except Exception as e:
            self.logger.error(f"Error during EventHandler cleanup: {e}\n{traceback.format_exc()}")

    def on_group_changed(self, index):
        """グループ変更時の処理"""
        self.logger.debug(f"Group changed to index {index}")
        if index >= 0 and self.main_window:
            try:
                self.main_window.data_handler.refresh_user_list()
            except Exception as e:
                self.logger.error(f"Error handling group change: {e}\n{traceback.format_exc()}")

    def add_user(self):
        """ユーザー追加"""
        if not self.main_window:
            return

        self.logger.debug("Starting user addition")
        try:
            left_pane = self.main_window.left_pane
            group_id = left_pane.get_current_group_id()

            if group_id is None:
                self.logger.warning("No group selected for user addition")
                QMessageBox.warning(self.main_window, "警告", "グループを選択してください")
                return

            name, ok = QInputDialog.getText(
                self.main_window,
                "ユーザー追加",
                "ユーザー名を入力してください:"
            )

            if ok and name.strip():
                self.logger.debug(f"Adding user '{name}' to group {group_id}")
                if self.db.add_user(name.strip(), group_id):
                    self.logger.info(f"Successfully added user '{name}'")
                    self.main_window.data_changed.emit()
                    QMessageBox.information(
                        self.main_window,
                        "成功",
                        f"ユーザー '{name}' を追加しました"
                    )
                else:
                    self.logger.error("Failed to add user")
                    QMessageBox.warning(
                        self.main_window,
                        "警告",
                        "ユーザーの追加に失敗しました"
                    )

        except Exception as e:
            self.logger.error(f"Error adding user: {e}\n{traceback.format_exc()}")
            QMessageBox.critical(
                self.main_window,
                "エラー",
                "ユーザーの追加中にエラーが発生しました"
            )

    def edit_user(self):
        """ユーザー編集"""
        if not self.main_window:
            return

        self.logger.debug("Starting user edit")
        try:
            left_pane = self.main_window.left_pane
            current_item = left_pane.get_selected_user()

            if not current_item:
                self.logger.warning("No user selected for editing")
                QMessageBox.warning(
                    self.main_window,
                    "警告",
                    "編集するユーザーを選択してください"
                )
                return

            user_id = current_item.data(Qt.ItemDataRole.UserRole)
            current_name = current_item.text()

            new_name, ok = QInputDialog.getText(
                self.main_window,
                "ユーザー編集",
                "新しいユーザー名を入力してください:",
                text=current_name
            )

            if ok and new_name.strip():
                self.logger.debug(f"Editing user {user_id} name to '{new_name}'")
                if self.db.edit_user(user_id, new_name.strip()):
                    self.logger.info(f"Successfully edited user {user_id}")
                    self.main_window.data_changed.emit()
                    QMessageBox.information(
                        self.main_window,
                        "成功",
                        f"ユーザー名を '{new_name}' に変更しました"
                    )
                else:
                    self.logger.error(f"Failed to edit user {user_id}")
                    QMessageBox.warning(
                        self.main_window,
                        "警告",
                        "ユーザーの編集に失敗しました"
                    )

        except Exception as e:
            self.logger.error(f"Error editing user: {e}\n{traceback.format_exc()}")
            QMessageBox.critical(
                self.main_window,
                "エラー",
                "ユーザーの編集中にエラーが発生しました"
            )

    def delete_user(self):
        """ユーザー削除"""
        if not self.main_window:
            return

        self.logger.debug("Starting user deletion")
        try:
            left_pane = self.main_window.left_pane
            current_item = left_pane.get_selected_user()

            if not current_item:
                self.logger.warning("No user selected for deletion")
                QMessageBox.warning(
                    self.main_window,
                    "警告",
                    "削除するユーザーを選択してください"
                )
                return

            user_id = current_item.data(Qt.ItemDataRole.UserRole)
            user_name = current_item.text()

            reply = QMessageBox.question(
                self.main_window,
                "確認",
                f"ユーザー '{user_name}' を削除してもよろしいですか？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.logger.debug(f"Deleting user {user_id}")
                if self.db.delete_user(user_id):
                    self.logger.info(f"Successfully deleted user {user_id}")
                    self.main_window.user_deleted.emit(user_id)
                    self.main_window.data_changed.emit()
                    QMessageBox.information(
                        self.main_window,
                        "成功",
                        f"ユーザー '{user_name}' を削除しました"
                    )
                else:
                    self.logger.error(f"Failed to delete user {user_id}")
                    QMessageBox.warning(
                        self.main_window,
                        "警告",
                        "ユーザーの削除に失敗しました"
                    )

        except Exception as e:
            self.logger.error(f"Error deleting user: {e}\n{traceback.format_exc()}")
            QMessageBox.critical(
                self.main_window,
                "エラー",
                "ユーザーの削除中にエラーが発生しました"
            )
