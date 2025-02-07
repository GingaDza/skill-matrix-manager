from PyQt6.QtWidgets import QMessageBox, QListWidgetItem
from PyQt6.QtCore import QObject, Qt, QTimer, QMetaObject, QCoreApplication, QThread
import logging
import traceback
from typing import Optional, Dict, Any
import psutil
import json
import os

class DataHandler(QObject):
    """データ操作を管理するハンドラー"""
    def __init__(self, db, main_window):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.db = db
        self._main_window = main_window
        self.is_updating = False
        
        # デバッグ情報
        self._debug_info: Dict[str, Any] = {
            'update_count': 0,
            'last_error': None,
            'memory_stats': {},
            'ui_state': {}
        }
        
        # 更新キューの管理
        self._update_scheduled = False
        self._update_timer = QTimer(self)
        self._update_timer.setSingleShot(True)
        self._update_timer.timeout.connect(self._process_update)
        
        # 状態管理
        self._last_group_id = None
        self._last_user_id = None
        self._update_depth = 0
        
        # デバッグログの設定
        self._setup_debug_logging()

    def _setup_debug_logging(self):
        """デバッグログの設定"""
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # ファイルハンドラの追加
        debug_dir = 'debug_logs'
        os.makedirs(debug_dir, exist_ok=True)
        file_handler = logging.FileHandler(
            os.path.join(debug_dir, 'data_handler_debug.log')
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def _log_debug_state(self, action: str):
        """現在の状態をログに記録"""
        self._debug_info['update_count'] += 1
        current_memory = self._get_memory_usage()
        self._debug_info['memory_stats'] = current_memory
        
        self.logger.debug(
            f"Action: {action}\n"
            f"Update count: {self._debug_info['update_count']}\n"
            f"Is updating: {self.is_updating}\n"
            f"Update scheduled: {self._update_scheduled}\n"
            f"Update depth: {self._update_depth}\n"
            f"Last group ID: {self._last_group_id}\n"
            f"Last user ID: {self._last_user_id}\n"
            f"Current thread: {QThread.currentThread().objectName()}\n"
            f"Memory RSS: {current_memory['rss'] / 1024 / 1024:.2f} MB\n"
            f"Memory VMS: {current_memory['vms'] / 1024 / 1024:.2f} MB"
        )

    def _get_memory_usage(self) -> Dict[str, int]:
        """メモリ使用状況の取得"""
        process = psutil.Process()
        memory_info = process.memory_info()
        return {
            'rss': memory_info.rss,
            'vms': memory_info.vms
        }

    def schedule_update(self, immediate: bool = False):
        """更新をスケジュール"""
        self._log_debug_state("schedule_update")
        
        if self._update_depth > 5:
            self.logger.warning("Update depth limit exceeded")
            return
            
        if not self._update_scheduled:
            self._update_scheduled = True
            interval = 0 if immediate else 100
            self._update_timer.start(interval)

    def _process_update(self):
        """更新処理の実行"""
        self._log_debug_state("process_update")
        
        try:
            self._update_scheduled = False
            self._update_depth += 1
            self._safe_refresh()
        except Exception as e:
            self.logger.error(f"Error processing update: {e}", exc_info=True)
            self._debug_info['last_error'] = str(e)
        finally:
            self._update_depth -= 1
            self.is_updating = False

    def _safe_refresh(self):
        """安全なデータ更新の実行"""
        self._log_debug_state("safe_refresh")
        
        if self.is_updating:
            self.logger.debug("Update already in progress")
            return

        self.is_updating = True
        
        try:
            if not self._main_window:
                self.logger.warning("Main window reference lost")
                return

            if not QThread.currentThread() == QCoreApplication.instance().thread():
                self.logger.warning("Attempting to update UI from non-UI thread")
                QMetaObject.invokeMethod(
                    self,
                    "_safe_refresh",
                    Qt.ConnectionType.QueuedConnection
                )
                return

            self._capture_ui_state()
            self._update_groups()
            self._update_users()
            self._restore_ui_state()
            
            self.logger.debug("Data refresh completed successfully")

        except Exception as e:
            self.logger.error(f"Error refreshing data: {e}", exc_info=True)
            self._debug_info['last_error'] = str(e)
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

    def _capture_ui_state(self):
        """UI状態の保存"""
        try:
            left_pane = self._main_window.left_pane
            self._debug_info['ui_state'] = {
                'group_index': left_pane.group_combo.currentIndex(),
                'user_row': left_pane.user_list.currentRow(),
                'group_id': self._last_group_id,
                'user_id': self._last_user_id
            }
        except Exception as e:
            self.logger.error(f"Error capturing UI state: {e}", exc_info=True)

    def _restore_ui_state(self):
        """UI状態の復元"""
        try:
            ui_state = self._debug_info['ui_state']
            left_pane = self._main_window.left_pane
            
            if ui_state.get('group_index') >= 0:
                left_pane.group_combo.setCurrentIndex(ui_state['group_index'])
            if ui_state.get('user_row') >= 0:
                left_pane.user_list.setCurrentRow(ui_state['user_row'])
                
            self._last_group_id = ui_state.get('group_id')
            self._last_user_id = ui_state.get('user_id')
        except Exception as e:
            self.logger.error(f"Error restoring UI state: {e}", exc_info=True)

    def _show_error(self, message: str):
        """エラーメッセージの表示"""
        if self._main_window:
            try:
                QMessageBox.critical(self._main_window, "エラー", message)
            except Exception as e:
                self.logger.error(f"Error showing error message: {e}", exc_info=True)

    def load_initial_data(self):
        """初期データの読み込み"""
        self.logger.debug("Loading initial data")
        self.schedule_update(immediate=True)

    def refresh_data(self):
        """データの更新をリクエスト"""
        self.logger.debug("Refresh data requested")
        self.schedule_update()

    def refresh_user_list(self):
        """ユーザーリストの更新をリクエスト"""
        self.logger.debug("User list refresh requested")
        if not self.is_updating:
            self._update_users()

    def cleanup(self):
        """リソースのクリーンアップ"""
        self._log_debug_state("cleanup")
        
        try:
            self.is_updating = False
            self._update_scheduled = False
            if self._update_timer and self._update_timer.isActive():
                self._update_timer.stop()
            if self._update_timer:
                self._update_timer.deleteLater()
            self._update_timer = None
            self._main_window = None
            self.db = None
            
            # デバッグ情報の保存
            self._save_debug_info()
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}", exc_info=True)

    def _save_debug_info(self):
        """デバッグ情報の保存"""
        try:
            debug_dir = 'debug_logs'
            os.makedirs(debug_dir, exist_ok=True)
            debug_file = os.path.join(debug_dir, 'data_handler_debug.json')
            
            with open(debug_file, 'w', encoding='utf-8') as f:
                json.dump(self._debug_info, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Error saving debug info: {e}", exc_info=True)
