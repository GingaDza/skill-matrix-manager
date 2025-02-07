from PyQt6.QtWidgets import QMessageBox, QListWidgetItem
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
            self.logger.debug("Update already in progress, skipping")
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
                self.logger.debug(f"Adding group: {group_id} - {group_name}")
                left_pane.group_combo.addItem(group_name, group_id)

            # 現在のグループを再選択
            if current_group_id is not None:
                index = left_pane.group_combo.findData(current_group_id)
                if index >= 0:
                    left_pane.group_combo.setCurrentIndex(index)
                    self.logger.debug(f"Restored selection to group ID: {current_group_id}")
            elif left_pane.group_combo.count() > 0:
                left_pane.group_combo.setCurrentIndex(0)
                self.logger.debug("Set initial group selection")

            self.refresh_user_list()
            self.logger.debug("Data refresh completed successfully")

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
                self.logger.debug("No group selected, clearing user list")
                left_pane.user_list.clear()
                return

            self.logger.debug(f"Fetching users for group {group_id}")
            users = self.db.get_users_by_group(group_id)
            self.logger.debug(f"Found {len(users)} users")

            left_pane.user_list.clear()
            for user_id, user_name in users:
                self.logger.debug(f"Adding user: {user_id} - {user_name}")
                item = QListWidgetItem(user_name)
                item.setData(Qt.ItemDataRole.UserRole, user_id)
                left_pane.user_list.addItem(item)

        except Exception as e:
            self.logger.error(f"Error refreshing user list: {e}\n{traceback.format_exc()}")
            raise
