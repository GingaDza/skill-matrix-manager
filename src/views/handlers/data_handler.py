from PyQt6.QtWidgets import QMessageBox, QListWidgetItem
from PyQt6.QtCore import QObject, Qt, QTimer, QMetaObject, QCoreApplication, QThread
import logging
import traceback
from typing import Optional, Dict, Any, List, Tuple
import psutil
import json
import os
import gc
import weakref

class DataHandler(QObject):
    """データ操作を管理するハンドラー"""
    def __init__(self, db, main_window):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.db = db
        self._main_window = main_window
        
        # メモリ管理
        self._cache: Dict[str, Any] = {}
        self._last_update_time = 0
        self.is_updating = False
        
        # 更新キューの管理
        self._update_scheduled = False
        self._update_timer = QTimer(self)
        self._update_timer.setSingleShot(True)
        self._update_timer.timeout.connect(self._process_update)
        
        # 状態管理
        self._last_group_id = None
        self._last_user_id = None
        self._update_depth = 0
        
        # デバッグ設定
        self._setup_debug()

    def _setup_debug(self):
        """デバッグ環境の設定"""
        # ログ設定
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # ログディレクトリ作成
        debug_dir = 'debug_logs'
        os.makedirs(debug_dir, exist_ok=True)
        
        # ファイルハンドラ
        file_handler = logging.FileHandler(
            os.path.join(debug_dir, 'data_handler.log'),
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # メモリ監視初期設定
        self._initial_memory = self._get_memory_usage()
        self._log_memory_usage("初期化完了")

    def _get_memory_usage(self) -> Dict[str, float]:
        """メモリ使用状況を取得"""
        process = psutil.Process()
        memory_info = process.memory_info()
        return {
            'rss': memory_info.rss / (1024 * 1024),  # MB
            'vms': memory_info.vms / (1024 * 1024)   # MB
        }

    def _log_memory_usage(self, action: str):
        """メモリ使用状況をログに記録"""
        current_memory = self._get_memory_usage()
        memory_diff = {
            key: current_memory[key] - self._initial_memory[key]
            for key in current_memory
        }
        
        self.logger.debug(
            f"Memory Usage ({action}):\n"
            f"  Current RSS: {current_memory['rss']:.2f} MB "
            f"(Diff: {memory_diff['rss']:+.2f} MB)\n"
            f"  Current VMS: {current_memory['vms']:.2f} MB "
            f"(Diff: {memory_diff['vms']:+.2f} MB)"
        )

    def schedule_update(self, immediate: bool = False):
        """更新をスケジュール"""
        try:
            if self._update_depth > 5:
                self.logger.warning("更新の深さ制限を超過")
                return
                
            if not self._update_scheduled:
                self._update_scheduled = True
                interval = 0 if immediate else 100
                self._update_timer.start(interval)
                self._log_memory_usage("更新スケジュール")
                
        except Exception as e:
            self.logger.error(f"更新スケジュール中のエラー: {e}", exc_info=True)

    def _process_update(self):
        """更新処理の実行"""
        try:
            self._update_scheduled = False
            self._update_depth += 1
            self._safe_refresh()
            self._log_memory_usage("更新処理完了")
            
        except Exception as e:
            self.logger.error(f"更新処理中のエラー: {e}", exc_info=True)
            
        finally:
            self._update_depth -= 1
            self.is_updating = False
            gc.collect()  # 明示的なガベージコレクション

    def _safe_refresh(self):
        """安全なデータ更新の実行"""
        if self.is_updating:
            return

        self.is_updating = True
        self._log_memory_usage("更新開始")
        
        try:
            if not self._main_window:
                return

            # UIスレッドチェック
            if QThread.currentThread() != QCoreApplication.instance().thread():
                QMetaObject.invokeMethod(
                    self,
                    "_safe_refresh",
                    Qt.ConnectionType.QueuedConnection
                )
                return

            self._update_ui()
            self._log_memory_usage("UI更新完了")
            
        except Exception as e:
            self.logger.error(f"データ更新中のエラー: {e}", exc_info=True)
            self._show_error("データの更新に失敗しました")
            
        finally:
            self.is_updating = False
            self._cleanup_cache()

    def _update_ui(self):
        """UI更新の実行"""
        try:
            left_pane = self._main_window.left_pane
            
            # グループ更新
            groups = self._fetch_groups()
            self._update_groups(groups, left_pane)
            
            # ユーザー更新
            group_id = self._last_group_id or left_pane.get_current_group_id()
            if group_id:
                users = self._fetch_users(group_id)
                self._update_users(users, left_pane)
                
            left_pane.update_button_states()
            
        except Exception as e:
            self.logger.error(f"UI更新中のエラー: {e}", exc_info=True)
            raise

    def _fetch_groups(self) -> List[Tuple[int, str]]:
        """グループデータの取得"""
        return self.db.get_all_groups()

    def _fetch_users(self, group_id: int) -> List[Tuple[int, str]]:
        """ユーザーデータの取得"""
        return self.db.get_users_by_group(group_id)

    def _update_groups(self, groups: List[Tuple[int, str]], left_pane):
        """グループUIの更新"""
        current_group_id = self._last_group_id or left_pane.get_current_group_id()
        
        left_pane.group_combo.blockSignals(True)
        try:
            left_pane.group_combo.clear()
            for group_id, group_name in groups:
                left_pane.group_combo.addItem(group_name, group_id)

            if current_group_id:
                index = left_pane.group_combo.findData(current_group_id)
                if index >= 0:
                    left_pane.group_combo.setCurrentIndex(index)
                    self._last_group_id = current_group_id
        finally:
            left_pane.group_combo.blockSignals(False)

    def _update_users(self, users: List[Tuple[int, str]], left_pane):
        """ユーザーリストUIの更新"""
        current_row = left_pane.user_list.currentRow()
        
        left_pane.user_list.blockSignals(True)
        try:
            left_pane.user_list.clear()
            for user_id, user_name in users:
                item = QListWidgetItem(user_name)
                item.setData(Qt.ItemDataRole.UserRole, user_id)
                left_pane.user_list.addItem(item)

            if 0 <= current_row < left_pane.user_list.count():
                left_pane.user_list.setCurrentRow(current_row)
        finally:
            left_pane.user_list.blockSignals(False)

    def _cleanup_cache(self):
        """キャッシュのクリーンアップ"""
        try:
            self._cache.clear()
            gc.collect()
            self._log_memory_usage("キャッシュクリーンアップ")
        except Exception as e:
            self.logger.error(f"キャッシュクリーンアップ中のエラー: {e}", exc_info=True)

    def _show_error(self, message: str):
        """エラーメッセージの表示"""
        if self._main_window:
            try:
                QMessageBox.critical(self._main_window, "エラー", message)
            except Exception as e:
                self.logger.error(f"エラー表示中の問題: {e}", exc_info=True)

    def cleanup(self):
        """リソースのクリーンアップ"""
        try:
            self._log_memory_usage("クリーンアップ開始")
            
            self.is_updating = False
            self._update_scheduled = False
            
            if self._update_timer:
                if self._update_timer.isActive():
                    self._update_timer.stop()
                self._update_timer.deleteLater()
                self._update_timer = None
            
            self._main_window = None
            self.db = None
            self._cache.clear()
            
            gc.collect()
            self._log_memory_usage("クリーンアップ完了")
            
        except Exception as e:
            self.logger.error(f"クリーンアップ中のエラー: {e}", exc_info=True)

    def load_initial_data(self):
        """初期データの読み込み"""
        self.logger.debug("初期データ読み込み開始")
        self.schedule_update(immediate=True)

    def refresh_data(self):
        """データの更新をリクエスト"""
        self.logger.debug("データ更新リクエスト受信")
        self.schedule_update()

    def refresh_user_list(self):
        """ユーザーリストの更新をリクエスト"""
        self.logger.debug("ユーザーリスト更新リクエスト受信")
        if not self.is_updating:
            self._update_users(
                self._fetch_users(self._last_group_id),
                self._main_window.left_pane
            )
