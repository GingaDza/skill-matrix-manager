from PyQt6.QtWidgets import QMessageBox, QListWidgetItem
from PyQt6.QtCore import QObject, Qt, QTimer
import logging
import traceback

class DataHandler(QObject):
    """データ操作を管理するハンドラー"""
    def __init__(self, db, main_window):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.db = db
        self._main_window = main_window
        self.is_updating = False
        
        # 遅延更新用タイマー
        self._update_timer = QTimer(self)
        self._update_timer.setSingleShot(True)
        self._update_timer.timeout.connect(self._delayed_refresh)
        
        # 前回の状態
        self._last_group_id = None

    def cleanup(self):
        """リソースのクリーンアップ"""
        self.logger.debug("Cleaning up DataHandler")
        try:
            self.is_updating = False
            if self._update_timer.isActive():
                self._update_timer.stop()
            self._update_timer = None
            self._main_window = None
            self.db = None
        except Exception as e:
            self.logger.error(f"Error during DataHandler cleanup: {e}", exc_info=True)

    def load_initial_data(self):
        """初期データの読み込み"""
        self.logger.debug("Loading initial data")
        self._safe_refresh()

    def refresh_data(self):
        """データの更新をスケジュール"""
        if self.is_updating:
            self.logger.debug("Update already scheduled")
            return
            
        self.is_updating = True
        self._update_timer.start(100)  # 100ms後に更新

    def _delayed_refresh(self):
        """遅延更新の実行"""
        try:
            self._safe_refresh()
        finally:
            self.is_updating = False

    def _safe_refresh(self):
        """安全なデータ更新の実行"""
        self.logger.debug("Starting safe data refresh")
        try:
            # グループデータの更新
            groups = self.db.get_all_groups()
            self.logger.debug(f"Fetched {len(groups)} groups")

            left_pane = self._main_window.left_pane
            current_group_id = self._last_group_id or left_pane.get_current_group_id()

            # シグナルをブロック
            left_pane.group_combo.blockSignals(True)
            try:
                left_pane.group_combo.clear()
                for group_id, group_name in groups:
                    self.logger.debug(f"Adding group: {group_id} - {group_name}")
                    left_pane.group_combo.addItem(group_name, group_id)

                if current_group_id is not None:
                    index = left_pane.group_combo.findData(current_group_id)
                    if index >= 0:
                        left_pane.group_combo.setCurrentIndex(index)
                        self._last_group_id = current_group_id
                        self.logger.debug(f"Restored selection to group ID: {current_group_id}")
                elif left_pane.group_combo.count() > 0:
                    left_pane.group_combo.setCurrentIndex(0)
                    self._last_group_id = left_pane.group_combo.currentData()
                    self.logger.debug(f"Set initial group selection: {self._last_group_id}")
            finally:
                left_pane.group_combo.blockSignals(False)

            self._safe_refresh_user_list()
            self.logger.debug("Data refresh completed successfully")

        except Exception as e:
            self.logger.error(f"Error refreshing data: {e}", exc_info=True)
            if self._main_window:
                QMessageBox.critical(self._main_window, "エラー", "データの更新に失敗しました")

    def _safe_refresh_user_list(self):
        """安全なユーザーリストの更新"""
        try:
            left_pane = self._main_window.left_pane
            group_id = self._last_group_id or left_pane.get_current_group_id()

            if group_id is None:
                self.logger.debug("No group selected, clearing user list")
                left_pane.user_list.clear()
                return

            self.logger.debug(f"Fetching users for group {group_id}")
            users = self.db.get_users_by_group(group_id)
            self.logger.debug(f"Found {len(users)} users")

            # ユーザーリストを更新
            left_pane.user_list.clear()
            for user_id, user_name in users:
                self.logger.debug(f"Adding user: {user_id} - {user_name}")
                item = QListWidgetItem(user_name)
                item.setData(Qt.ItemDataRole.UserRole, user_id)
                left_pane.user_list.addItem(item)

            # ボタン状態を更新
            left_pane.update_button_states()

        except Exception as e:
            self.logger.error(f"Error refreshing user list: {e}", exc_info=True)
            raise

    def refresh_user_list(self):
        """ユーザーリストの更新をスケジュール"""
        if not self.is_updating:
            self._safe_refresh_user_list()
