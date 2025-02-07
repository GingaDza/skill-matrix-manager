from PyQt6.QtWidgets import QMessageBox, QListWidgetItem
from PyQt6.QtCore import QObject, Qt, QTimer, QMetaObject, QCoreApplication
import logging
import traceback
from typing import Optional, Dict, Any
import weakref
import sys

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
        file_handler = logging.FileHandler('data_handler_debug.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def _log_debug_state(self, action: str):
        """現在の状態をログに記録"""
        self._debug_info['update_count'] += 1
        self.logger.debug(
            f"Action: {action}\n"
            f"Update count: {self._debug_info['update_count']}\n"
            f"Is updating: {self.is_updating}\n"
            f"Update scheduled: {self._update_scheduled}\n"
            f"Update depth: {self._update_depth}\n"
            f"Last group ID: {self._last_group_id}\n"
            f"Last user ID: {self._last_user_id}\n"
            f"Current thread: {QThread.currentThread().objectName()}\n"
            f"Memory usage: {self._get_memory_usage()}"
        )

    def _get_memory_usage(self) -> Dict[str, int]:
        """メモリ使用状況の取得"""
        import psutil
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
            import json
            with open('data_handler_debug.json', 'w') as f:
                json.dump(self._debug_info, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving debug info: {e}", exc_info=True)

[残りのコードは同じ...]
