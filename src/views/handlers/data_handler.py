from PyQt6.QtWidgets import QMessageBox, QListWidgetItem
from PyQt6.QtCore import (
    QObject, Qt, QTimer, QThread, QMetaObject,
    QCoreApplication, pyqtSignal, pyqtSlot
)
import logging
import traceback
from typing import Optional, Dict, Any, List, Tuple
import psutil
import json
import os
import gc
import sys
import weakref
from datetime import datetime
from functools import partial
from src.utils.memory_tracker import MemoryTracker

class UpdateWorker(QThread):
    """非同期更新処理を行うワーカー"""
    update_completed = pyqtSignal(list, list)
    error_occurred = pyqtSignal(str)

    def __init__(self, db, group_id=None):
        super().__init__()
        self.db = db
        self.group_id = group_id

    def run(self):
        try:
            groups = self.db.get_all_groups()
            users = []
            if self.group_id is not None:
                users = self.db.get_users_by_group(self.group_id)
            self.update_completed.emit(groups, users)
        except Exception as e:
            self.error_occurred.emit(str(e))

class DataHandler(QObject):
    """データ操作を管理するハンドラー"""
    update_started = pyqtSignal()
    update_finished = pyqtSignal()

    def __init__(self, db, main_window):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.memory_tracker = MemoryTracker()
        
        # 基本設定
        self.db = db
        self._main_window = main_window
        self.is_updating = False
        
        # メモリ管理
        self._cache = {}
        self._workers = []
        self._update_count = 0
        self._last_cleanup_time = datetime.now()
        
        # 状態管理
        self._last_group_id = None
        self._last_user_id = None
        self._pending_updates = 0
        
        # タイマー設定
        self._setup_timers()
        self._setup_debug()
        
        self.memory_tracker.track_object(self, "DataHandler")
        self.memory_tracker.log_tracking_info("DataHandler初期化完了")

    def _setup_timers(self):
        """タイマーの初期化"""
        # 更新スケジューラ
        self._update_timer = QTimer(self)
        self._update_timer.setSingleShot(True)
        self._update_timer.timeout.connect(self._process_update)
        
        # メモリ監視
        self._memory_timer = QTimer(self)
        self._memory_timer.timeout.connect(self._check_memory)
        self._memory_timer.start(2000)
        
        # 自動クリーンアップ
        self._cleanup_timer = QTimer(self)
        self._cleanup_timer.timeout.connect(self._auto_cleanup)
        self._cleanup_timer.start(5000)
        
        # メモリ詳細チェック
        self._memory_check_timer = QTimer(self)
        self._memory_check_timer.timeout.connect(self._check_memory_detailed)
        self._memory_check_timer.start(1000)

    def _setup_debug(self):
        """デバッグ環境の設定"""
        self.logger.setLevel(logging.DEBUG)
        debug_dir = os.path.join('debug_logs', datetime.now().strftime('%Y%m%d'))
        os.makedirs(debug_dir, exist_ok=True)
        
        handler = logging.FileHandler(
            os.path.join(debug_dir, f'data_handler_{datetime.now().strftime("%H%M%S")}.log'),
            encoding='utf-8'
        )
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - [%(threadName)s] %(message)s'
        ))
        self.logger.addHandler(handler)

    def _check_memory_detailed(self):
        """詳細なメモリチェック"""
        try:
            self.memory_tracker.take_snapshot(f"定期チェック_{self._update_count}")
            self.memory_tracker.log_tracking_info("定期メモリチェック")
            
            if self._update_count % 10 == 0:
                self.memory_tracker.check_leaks()
                
        except Exception as e:
            self.logger.error(f"詳細メモリチェックエラー: {e}")

    def _check_memory(self):
        """メモリ使用状況のチェック"""
        try:
            mem = self.memory_tracker.get_memory_usage()
            if mem.get('rss', 0) > 150:  # 150MB超過で緊急クリーンアップ
                self._force_cleanup()
        except Exception as e:
            self.logger.error(f"メモリチェックエラー: {e}")

    def _force_cleanup(self):
        """強制メモリクリーンアップ"""
        try:
            self.logger.info("強制クリーンアップ開始")
            self._cache.clear()
            self._cleanup_workers()
            gc.collect()
            self.memory_tracker.log_tracking_info("強制クリーンアップ完了")
        except Exception as e:
            self.logger.error(f"強制クリーンアップエラー: {e}")

    def _auto_cleanup(self):
        """定期的なクリーンアップ"""
        try:
            self._cleanup_workers()
            if len(self._cache) > 100:
                self._cache.clear()
            gc.collect()
        except Exception as e:
            self.logger.error(f"自動クリーンアップエラー: {e}")

    def _cleanup_workers(self):
        """完了したワーカーのクリーンアップ"""
        try:
            active_workers = []
            for worker in self._workers:
                if worker.isRunning():
                    active_workers.append(worker)
                else:
                    self.memory_tracker.untrack_object(worker, "UpdateWorker")
                    worker.deleteLater()
            self._workers = active_workers
        except Exception as e:
            self.logger.error(f"ワーカークリーンアップエラー: {e}")

    def _process_update(self):
        """更新処理の実行"""
        if self.is_updating:
            return

        try:
            self.is_updating = True
            self.update_started.emit()
            
            self.memory_tracker.take_snapshot(f"更新開始_{self._update_count}")
            
            worker = UpdateWorker(self.db, self._last_group_id)
            self.memory_tracker.track_object(worker, "UpdateWorker")
            
            worker.update_completed.connect(self._handle_update_completed)
            worker.error_occurred.connect(self._handle_update_error)
            worker.finished.connect(lambda: self._cleanup_worker(worker))
            
            self._workers.append(worker)
            worker.start()
            
            self._update_count += 1
            
        except Exception as e:
            self.logger.error(f"更新処理エラー: {e}")
            self.is_updating = False
            self._show_error("データ更新エラー")

    def _cleanup_worker(self, worker):
        """個別ワーカーのクリーンアップ"""
        try:
            self.memory_tracker.untrack_object(worker, "UpdateWorker")
            worker.deleteLater()
            if worker in self._workers:
                self._workers.remove(worker)
        except Exception as e:
            self.logger.error(f"ワーカークリーンアップエラー: {e}")

    @pyqtSlot(list, list)
    def _handle_update_completed(self, groups, users):
        """更新完了時の処理"""
        try:
            if not self._main_window:
                return

            left_pane = self._main_window.left_pane
            
            # グループ更新
            left_pane.group_combo.blockSignals(True)
            try:
                left_pane.group_combo.clear()
                for group_id, group_name in groups:
                    left_pane.group_combo.addItem(group_name, group_id)
                    
                if self._last_group_id:
                    index = left_pane.group_combo.findData(self._last_group_id)
                    if index >= 0:
                        left_pane.group_combo.setCurrentIndex(index)
            finally:
                left_pane.group_combo.blockSignals(False)

            # ユーザー更新
            if users:
                left_pane.user_list.blockSignals(True)
                try:
                    left_pane.user_list.clear()
                    for user_id, user_name in users:
                        item = QListWidgetItem(user_name)
                        item.setData(Qt.ItemDataRole.UserRole, user_id)
                        left_pane.user_list.addItem(item)
                finally:
                    left_pane.user_list.blockSignals(False)
                    
            left_pane.update_button_states()
            
            self.memory_tracker.take_snapshot(f"更新完了_{self._update_count}")
            
        except Exception as e:
            self.logger.error(f"更新完了処理エラー: {e}")
        finally:
            self.is_updating = False
            self.update_finished.emit()

    @pyqtSlot(str)
    def _handle_update_error(self, error_msg):
        """更新エラー時の処理"""
        self.logger.error(f"更新エラー: {error_msg}")
        self.is_updating = False
        self._show_error(f"データ更新エラー: {error_msg}")

    def _show_error(self, message: str):
        """エラーメッセージの表示"""
        try:
            QMessageBox.critical(None, "エラー", message)
        except Exception as e:
            self.logger.error(f"エラー表示失敗: {e}")

    def schedule_update(self, immediate: bool = False):
        """更新のスケジュール"""
        try:
            if not immediate and self.is_updating:
                return
                
            interval = 0 if immediate else 250
            self._update_timer.start(interval)
            self.memory_tracker.log_tracking_info("更新スケジュール")
            
        except Exception as e:
            self.logger.error(f"更新スケジュールエラー: {e}")

    def cleanup(self):
        """終了時のクリーンアップ"""
        try:
            self.memory_tracker.log_tracking_info("終了処理開始")
            
            # タイマーの停止
            for timer in [
                self._update_timer,
                self._memory_timer,
                self._cleanup_timer,
                self._memory_check_timer
            ]:
                timer.stop()
                timer.deleteLater()
            
            # ワーカーの停止
            for worker in self._workers:
                worker.quit()
                worker.wait()
                worker.deleteLater()
            
            self._workers.clear()
            self._cache.clear()
            self._main_window = None
            self.db = None
            
            self.memory_tracker.cleanup()
            gc.collect()
            
        except Exception as e:
            self.logger.error(f"終了処理エラー: {e}")

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
        if not self.is_updating and self._last_group_id:
            self.schedule_update()
