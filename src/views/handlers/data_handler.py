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
from datetime import datetime

class DataHandler(QObject):
    """データ操作を管理するハンドラー"""
    # クラス変数としてメモリ制限を定義
    MAX_MEMORY_RSS_MB = 200
    MAX_MEMORY_VMS_MB = 500
    CLEANUP_THRESHOLD_MB = 150

    def __init__(self, db, main_window):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._db = weakref.proxy(db)
        self._main_window = weakref.proxy(main_window)
        
        # メモリ管理
        self._cache = {}
        self._refs = weakref.WeakSet()
        self.is_updating = False
        
        # 更新管理
        self._update_scheduled = False
        self._update_timer = QTimer()
        self._update_timer.setSingleShot(True)
        self._update_timer.timeout.connect(self._process_update)
        self._refs.add(self._update_timer)
        
        # 状態管理
        self._last_group_id = None
        self._last_user_id = None
        self._update_depth = 0
        self._last_cleanup = datetime.now()
        
        # デバッグ設定
        self._setup_debug()
        
        # 定期的なメモリチェック
        self._memory_check_timer = QTimer()
        self._memory_check_timer.timeout.connect(self._check_memory_usage)
        self._memory_check_timer.start(5000)  # 5秒ごとにチェック
        self._refs.add(self._memory_check_timer)

    def _setup_debug(self):
        """デバッグ環境の設定"""
        self.logger.setLevel(logging.DEBUG)
        debug_dir = os.path.join('debug_logs', datetime.now().strftime('%Y%m%d'))
        os.makedirs(debug_dir, exist_ok=True)
        
        # ログファイルの設定
        log_file = os.path.join(
            debug_dir,
            f'data_handler_{datetime.now().strftime("%H%M%S")}.log'
        )
        handler = logging.FileHandler(log_file, encoding='utf-8')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(handler)
        
        # 初期メモリ状態の記録
        self._initial_memory = self._get_memory_usage()
        self._log_memory_state("初期化")

    def _get_memory_usage(self) -> Dict[str, float]:
        """メモリ使用状況を取得"""
        process = psutil.Process()
        memory_info = process.memory_info()
        return {
            'rss': memory_info.rss / (1024 * 1024),
            'vms': memory_info.vms / (1024 * 1024)
        }

    def _log_memory_state(self, action: str):
        """メモリ状態をログに記録"""
        try:
            current = self._get_memory_usage()
            diff = {
                key: current[key] - self._initial_memory[key]
                for key in current
            }
            
            self.logger.debug(
                f"Memory State ({action}):\n"
                f"  RSS: {current['rss']:.2f} MB (Diff: {diff['rss']:+.2f} MB)\n"
                f"  VMS: {current['vms']:.2f} MB (Diff: {diff['vms']:+.2f} MB)\n"
                f"  Objects in cache: {len(self._cache)}\n"
                f"  Weak references: {len(self._refs)}"
            )
        except Exception as e:
            self.logger.error(f"メモリログ記録エラー: {e}", exc_info=True)

    def _check_memory_usage(self):
        """メモリ使用量をチェックし、必要に応じて対策を実行"""
        try:
            current = self._get_memory_usage()
            
            if (current['rss'] > self.MAX_MEMORY_RSS_MB or
                current['vms'] > self.MAX_MEMORY_VMS_MB):
                self.logger.warning("メモリ使用量が制限を超過")
                self._force_cleanup()
                
            elif current['rss'] > self.CLEANUP_THRESHOLD_MB:
                self.logger.info("メモリ使用量が閾値を超過")
                self._cleanup_cache()
                
        except Exception as e:
            self.logger.error(f"メモリチェックエラー: {e}", exc_info=True)

    def _force_cleanup(self):
        """強制的なメモリクリーンアップを実行"""
        try:
            self.logger.info("強制クリーンアップ開始")
            
            # キャッシュのクリア
            self._cache.clear()
            
            # 弱参照の確認
            dead_refs = [ref for ref in self._refs if ref() is None]
            for ref in dead_refs:
                self._refs.remove(ref)
            
            # ガベージコレクションの実行
            gc.collect()
            
            self._log_memory_state("強制クリーンアップ後")
            
        except Exception as e:
            self.logger.error(f"強制クリーンアップエラー: {e}", exc_info=True)

    def _safe_update(self, func, *args, **kwargs):
        """安全な更新処理の実行"""
        try:
            if not self._main_window or not self._db:
                return
            
            result = func(*args, **kwargs)
            self._check_memory_usage()
            return result
            
        except Exception as e:
            self.logger.error(f"更新処理エラー: {e}", exc_info=True)
            self._show_error("更新処理に失敗しました")
            return None

    def schedule_update(self, immediate: bool = False):
        """更新をスケジュール"""
        def _schedule():
            if self._update_depth > 5:
                self.logger.warning("更新深度制限超過")
                return
                
            if not self._update_scheduled:
                self._update_scheduled = True
                interval = 0 if immediate else 100
                self._update_timer.start(interval)
                self._log_memory_state("更新スケジュール")
        
        self._safe_update(_schedule)

    def _process_update(self):
        """更新処理の実行"""
        def _process():
            self._update_scheduled = False
            self._update_depth += 1
            self._update_ui()
            self._update_depth -= 1
            self._log_memory_state("更新完了")
            
        self._safe_update(_process)

    def _update_ui(self):
        """UI更新の実行"""
        def _update():
            if not hasattr(self, '_main_window') or not self._main_window:
                return

            left_pane = self._main_window.left_pane
            
            # グループ更新
            with self._db_operation():
                groups = self._db.get_all_groups()
            self._update_groups(groups, left_pane)
            
            # ユーザー更新
            group_id = self._last_group_id or left_pane.get_current_group_id()
            if group_id:
                with self._db_operation():
                    users = self._db.get_users_by_group(group_id)
                self._update_users(users, left_pane)
            
            left_pane.update_button_states()
            
        self._safe_update(_update)

    def _update_groups(self, groups: List[Tuple[int, str]], left_pane):
        """グループUIの更新"""
        try:
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
                
        except Exception as e:
            self.logger.error(f"グループ更新エラー: {e}", exc_info=True)

    def _update_users(self, users: List[Tuple[int, str]], left_pane):
        """ユーザーリストUIの更新"""
        try:
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
                
        except Exception as e:
            self.logger.error(f"ユーザーリスト更新エラー: {e}", exc_info=True)

    def _show_error(self, message: str):
        """エラーメッセージの表示"""
        try:
            if self._main_window:
                QMessageBox.critical(self._main_window, "エラー", message)
        except Exception as e:
            self.logger.error(f"エラー表示失敗: {e}", exc_info=True)

    def cleanup(self):
        """リソースのクリーンアップ"""
        try:
            self._log_memory_state("クリーンアップ開始")
            
            # タイマーの停止
            if self._memory_check_timer:
                self._memory_check_timer.stop()
                self._memory_check_timer.deleteLater()
            if self._update_timer:
                self._update_timer.stop()
                self._update_timer.deleteLater()
            
            # 参照のクリア
            self._main_window = None
            self._db = None
            self._cache.clear()
            self._refs.clear()
            
            # 最終クリーンアップ
            gc.collect()
            self._log_memory_state("クリーンアップ完了")
            
        except Exception as e:
            self.logger.error(f"クリーンアップエラー: {e}", exc_info=True)

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
                self._db.get_users_by_group(self._last_group_id),
                self._main_window.left_pane
            )
