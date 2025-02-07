from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QObject, Qt
import logging
import traceback

class DataHandler(QObject):
    """データ操作を管理するハンドラー"""
    def __init__(self, db, main_window):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.db = db
        self.main_window = main_window
        self.is_updating = False

    def load_initial_data(self):
        """初期データの読み込み"""
        self.logger.debug("Loading initial data")
        self.refresh_data()

    def refresh_data(self):
        """データの更新"""
        if self.is_updating:
            return

        try:
            self.is_updating = True
            self.logger.debug("Refreshing data")

            # グループデータの更新
            groups = self.db.get_all_groups()
            self.logger.debug(f"Fetched {len(groups)} groups")

            left_pane = self.main_window.left_pane
            current_group_id = left_pane.get_current_group_id()

            left_pane.group_combo.clear()
            for group_id, group_name in groups:
                left_pane.group_combo.addItem(group_name, group_id)

            if current_group_id is not None:
                index = left_pane.group_combo.findData(current_group_id)
                if index >= 0:
                    left_pane.group_combo.setCurrentIndex(index)
            elif left_pane.group_combo.count() > 0:
                left_pane.group_combo.setCurrentIndex(0)

            self.refresh_user_list()

        except Exception as e:
            self.logger.error(f"Error refreshing data: {e}\n{traceback.format_exc()}")
            QMessageBox.critical(self.main_window, "エラー", "データの更新に失敗しました")
        finally:
            self.is_updating = False

    def refresh_user_list(self):
        """ユーザーリストの更新"""
        try:
            left_pane = self.main_window.left_pane
            group_id = left_pane.get_current_group_id()

            if group_id is None:
                left_pane.user_list.clear()
                return

            users = self.db.get_users_by_group(group_id)
            left_pane.user_list.clear()

            for user_id, user_name in users:
                item = left_pane.user_list.item(user_name)
                item.setData(Qt.ItemDataRole.UserRole, user_id)
                left_pane.user_list.addItem(item)

        except Exception as e:
            self.logger.error(f"Error refreshing user list: {e}\n{traceback.format_exc()}")
            raise
