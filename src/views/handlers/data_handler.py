from PyQt6.QtWidgets import QMessageBox, QListWidgetItem
from PyQt6.QtCore import QObject, Qt, QTimer, QMetaObject, Qt
import logging
import traceback
from typing import Optional

class DataHandler(QObject):
    """データ操作を管理するハンドラー"""
    def __init__(self, db, main_window):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.db = db
        self._main_window = main_window
        self.is_updating = False
        
        # 更新キューの管理
        self._update_scheduled = False
        self._update_timer = QTimer(self)
        self._update_timer.setSingleShot(True)
        self._update_timer.timeout.connect(self._process_update)
        
        # 前回の状態
        self._last_group_id = None
        self._last_user_id = None

    def cleanup(self):
        """リソースのクリーンアップ"""
        self.logger.debug("Cleaning up DataHandler")
        try:
            self.is_updating = False
            self._update_scheduled = False
            if self._update_timer.isActive():
                self._update_timer.stop()
            self._update_timer.deleteLater()
            self._update_timer = None
            self._main_window = None
            self.db = None
        except Exception as e:
            self.logger.error(f"Error during DataHandler cleanup: {e}", exc_info=True)

    def schedule_update(self, immediate: bool = False):
        """更新をスケジュール"""
        if not self._update_scheduled:
            self._update_scheduled = True
            interval = 0 if immediate else 100
            self._update_timer.start(interval)

    def _process_update(self):
        """更新処理の実行"""
        try:
            self._update_scheduled = False
            self._safe_refresh()
        except Exception as e:
            self.logger.error(f"Error processing update: {e}", exc_info=True)
        finally:
            self.is_updating = False

    def load_initial_data(self):
        """初期データの読み込み"""
        self.logger.debug("Loading initial data")
        self.schedule_update(immediate=True)

    def refresh_data(self):
        """データの更新をリクエスト"""
        self.logger.debug("Refresh data requested")
        self.schedule_update()

    def _safe_refresh(self):
        """安全なデータ更新の実行"""
        if self.is_updating:
            self.logger.debug("Update already in progress")
            return

        self.logger.debug("Starting safe data refresh")
        self.is_updating = True
        
        try:
            # メインウィンドウが有効かチェック
            if not self._main_window:
                self.logger.warning("Main window reference lost")
                return

            # UIスレッドで実行されているか確認
            if not self._main_window.thread() == self.thread():
                self.logger.warning("Attempting to update UI from non-UI thread")
                QMetaObject.invokeMethod(self, "_safe_refresh", Qt.ConnectionType.QueuedConnection)
                return

            self._update_groups()
            self._update_users()
            
            self.logger.debug("Data refresh completed successfully")

        except Exception as e:
            self.logger.error(f"Error refreshing data: {e}", exc_info=True)
            self._show_error("データの更新に失敗しました")
        finally:
            self.is_updating = False

    def _update_groups(self):
        """グループデータの更新"""
        try:
            groups = self.db.get_all_groups()
            self.logger.debug(f"Fetched {len(groups)} groups")

            left_pane = self._main_window.left_pane
            current_group_id = self._last_group_id or left_pane.get_current_group_id()

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

        except Exception as e:
            self.logger.error(f"Error updating groups: {e}", exc_info=True)
            raise

    def _update_users(self):
        """ユーザーリストの更新"""
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

            current_row = left_pane.user_list.currentRow()
            left_pane.user_list.blockSignals(True)
            try:
                left_pane.user_list.clear()
                for user_id, user_name in users:
                    self.logger.debug(f"Adding user: {user_id} - {user_name}")
                    item = QListWidgetItem(user_name)
                    item.setData(Qt.ItemDataRole.UserRole, user_id)
                    left_pane.user_list.addItem(item)

                # 選択状態の復元
                if 0 <= current_row < left_pane.user_list.count():
                    left_pane.user_list.setCurrentRow(current_row)
            finally:
                left_pane.user_list.blockSignals(False)

            left_pane.update_button_states()

        except Exception as e:
            self.logger.error(f"Error updating users: {e}", exc_info=True)
            raise

    def _show_error(self, message: str):
        """エラーメッセージの表示"""
        if self._main_window:
            try:
                QMessageBox.critical(self._main_window, "エラー", message)
            except Exception as e:
                self.logger.error(f"Error showing error message: {e}", exc_info=True)

    def refresh_user_list(self):
        """ユーザーリストの更新をリクエスト"""
        self.logger.debug("User list refresh requested")
        if not self.is_updating:
            self._update_users()
