from PyQt6.QtWidgets import QMessageBox, QListWidgetItem
from PyQt6.QtCore import (
    QObject, Qt, QTimer, QThread, QMetaObject,
    QCoreApplication, pyqtSignal, pyqtSlot
)
import logging
import traceback
from typing import Optional, Dict, Any, List, Tuple, Set
import psutil
import json
import os
import gc
import sys
import weakref
from datetime import datetime
from functools import partial, lru_cache
from contextlib import contextmanager

class MemoryOptimizedWorker(QThread):
    """メモリ最適化された非同期ワーカー"""
    update_completed = pyqtSignal(list, list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, db, group_id=None):
        super().__init__()
        self._db = weakref.proxy(db)  # 弱参照を使用
        self.group_id = group_id
        self._cache = {}
        
    @lru_cache(maxsize=16)
    def _get_cached_data(self, group_id: int) -> List[Tuple[int, str]]:
        """キャッシュ付きデータ取得"""
        return self._db.get_users_by_group(group_id)

    def run(self):
        try:
            groups = self._db.get_all_groups()
            users = []
            if self.group_id is not None:
                users = self._get_cached_data(self.group_id)
            self.update_completed.emit(groups, users)
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self._cache.clear()
            gc.collect()

class MemoryOptimizedHandler(QObject):
    """メモリ最適化されたデータハンドラー"""
    update_started = pyqtSignal()
    update_finished = pyqtSignal()
    
    # メモリ制限
    MEMORY_LIMITS = {
        'rss': 100,    # RSS制限(MB)
        'vms': 300,    # VMS制限(MB)
        'cache': 50    # キャッシュ制限(項目数)
    }
    
    def __init__(self, db, main_window):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        # 基本設定（弱参照使用）
        self._db = weakref.proxy(db)
        self._main_window = weakref.proxy(main_window)
        
        # 状態管理
        self._workers: Set[QThread] = set()
        self._last_group_id = None
        self._is_updating = False
        self._update_count = 0
        
        # キャッシュ管理
        self._cache: Dict[str, Any] = {}
        self._cache_timestamps: Dict[str, datetime] = {}
        
        # タイマー設定
        self._setup_timers()
        self._setup_logging()

    def _setup_timers(self):
        """タイマーの初期化"""
        self._timers = {}
        
        # 更新タイマー
        update_timer = QTimer(self)
        update_timer.setSingleShot(True)
        update_timer.timeout.connect(self._process_update)
        self._timers['update'] = update_timer
        
        # クリーンアップタイマー
        cleanup_timer = QTimer(self)
        cleanup_timer.timeout.connect(self._auto_cleanup)
        cleanup_timer.start(5000)  # 5秒ごと
        self._timers['cleanup'] = cleanup_timer

    def _setup_logging(self):
        """ロギングの設定"""
        self.logger.setLevel(logging.DEBUG)
        log_dir = os.path.join('logs', datetime.now().strftime('%Y%m%d'))
        os.makedirs(log_dir, exist_ok=True)
        
        handler = logging.FileHandler(
            os.path.join(log_dir, 'memory_handler.log'),
            encoding='utf-8'
        )
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - [%(threadName)s] %(message)s'
        ))
        self.logger.addHandler(handler)

    @contextmanager
    def _update_lock(self):
        """更新ロックの管理"""
        if self._is_updating:
            yield False
            return
            
        self._is_updating = True
        try:
            yield True
        finally:
            self._is_updating = False

    def _check_memory(self) -> bool:
        """メモリ使用状況のチェック"""
        try:
            process = psutil.Process()
            mem = process.memory_info()
            
            rss_mb = mem.rss / (1024 * 1024)
            vms_mb = mem.vms / (1024 * 1024)
            
            if rss_mb > self.MEMORY_LIMITS['rss']:
                self._force_cleanup()
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"メモリチェックエラー: {e}")
            return False

    def _force_cleanup(self):
        """強制メモリクリーンアップ"""
        try:
            self.logger.info("強制クリーンアップ開始")
            
            # キャッシュクリア
            self._cache.clear()
            self._cache_timestamps.clear()
            
            # 完了したワーカーの削除
            self._cleanup_workers()
            
            # 明示的なGC
            gc.collect()
            
        except Exception as e:
            self.logger.error(f"強制クリーンアップエラー: {e}")

    def _cleanup_workers(self):
        """ワーカーのクリーンアップ"""
        try:
            completed = {w for w in self._workers if not w.isRunning()}
            for worker in completed:
                worker.deleteLater()
                self._workers.remove(worker)
        except Exception as e:
            self.logger.error(f"ワーカークリーンアップエラー: {e}")

    def _auto_cleanup(self):
        """自動クリーンアップ"""
        try:
            current_time = datetime.now()
            
            # 古いキャッシュの削除（30秒以上経過）
            self._cache = {
                k: v for k, v in self._cache.items()
                if (current_time - self._cache_timestamps[k]).seconds < 30
            }
            self._cache_timestamps = {
                k: v for k, v in self._cache_timestamps.items()
                if k in self._cache
            }
            
            # ワーカーのクリーンアップ
            self._cleanup_workers()
            
            # キャッシュサイズの制限
            if len(self._cache) > self.MEMORY_LIMITS['cache']:
                oldest_keys = sorted(
                    self._cache_timestamps.items(),
                    key=lambda x: x[1]
                )[:len(self._cache) - self.MEMORY_LIMITS['cache']]
                
                for k, _ in oldest_keys:
                    del self._cache[k]
                    del self._cache_timestamps[k]
                    
            gc.collect()
            
        except Exception as e:
            self.logger.error(f"自動クリーンアップエラー: {e}")

    @pyqtSlot()
    def _process_update(self):
        """更新処理の実行"""
        with self._update_lock() as locked:
            if not locked:
                return
                
            try:
                if not self._check_memory():
                    return
                    
                self.update_started.emit()
                self._update_count += 1
                
                worker = MemoryOptimizedWorker(self._db, self._last_group_id)
                worker.update_completed.connect(self._handle_update_completed)
                worker.error_occurred.connect(self._handle_update_error)
                worker.finished.connect(lambda: self._cleanup_worker(worker))
                
                self._workers.add(worker)
                worker.start()
                
            except Exception as e:
                self.logger.error(f"更新処理エラー: {e}")
                self._show_error("データ更新エラー")

    def _cleanup_worker(self, worker: QThread):
        """個別ワーカーのクリーンアップ"""
        try:
            worker.deleteLater()
            if worker in self._workers:
                self._workers.remove(worker)
        except Exception as e:
            self.logger.error(f"ワーカークリーンアップエラー: {e}")

    @pyqtSlot(list, list)
    def _handle_update_completed(self, groups: List[Tuple[int, str]], users: List[Tuple[int, str]]):
        """更新完了の処理"""
        try:
            if not self._main_window or not hasattr(self._main_window, 'left_pane'):
                return
                
            left_pane = self._main_window.left_pane
            
            # グループの更新
            with self._handle_ui_update():
                self._update_groups(groups, left_pane)
                if users:
                    self._update_users(users, left_pane)
                left_pane.update_button_states()
                
        except Exception as e:
            self.logger.error(f"更新完了処理エラー: {e}")
        finally:
            self.update_finished.emit()

    @contextmanager
    def _handle_ui_update(self):
        """UI更新のシグナルブロック管理"""
        try:
            left_pane = self._main_window.left_pane
            left_pane.group_combo.blockSignals(True)
            left_pane.user_list.blockSignals(True)
            yield
        finally:
            if hasattr(self, '_main_window') and self._main_window:
                left_pane = self._main_window.left_pane
                left_pane.group_combo.blockSignals(False)
                left_pane.user_list.blockSignals(False)

    def _update_groups(self, groups: List[Tuple[int, str]], left_pane):
        """グループリストの更新"""
        try:
            current_group_id = self._last_group_id
            
            left_pane.group_combo.clear()
            for group_id, group_name in groups:
                left_pane.group_combo.addItem(group_name, group_id)
                
            if current_group_id:
                index = left_pane.group_combo.findData(current_group_id)
                if index >= 0:
                    left_pane.group_combo.setCurrentIndex(index)
                    self._last_group_id = current_group_id
                    
            # キャッシュの更新
            cache_key = f'groups_{datetime.now().timestamp()}'
            self._cache[cache_key] = groups
            self._cache_timestamps[cache_key] = datetime.now()
            
        except Exception as e:
            self.logger.error(f"グループ更新エラー: {e}")

    def _update_users(self, users: List[Tuple[int, str]], left_pane):
        """ユーザーリストの更新"""
        try:
            current_row = left_pane.user_list.currentRow()
            
            left_pane.user_list.clear()
            for user_id, user_name in users:
                item = QListWidgetItem(user_name)
                item.setData(Qt.ItemDataRole.UserRole, user_id)
                left_pane.user_list.addItem(item)
                
            if 0 <= current_row < left_pane.user_list.count():
                left_pane.user_list.setCurrentRow(current_row)
                
            # キャッシュの更新
            if self._last_group_id:
                cache_key = f'users_{self._last_group_id}_{datetime.now().timestamp()}'
                self._cache[cache_key] = users
                self._cache_timestamps[cache_key] = datetime.now()
                
        except Exception as e:
            self.logger.error(f"ユーザーリスト更新エラー: {e}")

    @pyqtSlot(str)
    def _handle_update_error(self, error_msg: str):
        """エラー処理"""
        self.logger.error(f"更新エラー: {error_msg}")
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
            if not immediate and self._is_updating:
                return
                
            interval = 0 if immediate else 250
            self._timers['update'].start(interval)
            
        except Exception as e:
            self.logger.error(f"更新スケジュールエラー: {e}")

    def cleanup(self):
        """終了時のクリーンアップ"""
        try:
            self.logger.info("終了処理開始")
            
            # タイマーの停止
            for timer in self._timers.values():
                timer.stop()
                timer.deleteLater()
            self._timers.clear()
            
            # ワーカーの停止
            for worker in self._workers:
                worker.quit()
                worker.wait()
                worker.deleteLater()
            self._workers.clear()
            
            # キャッシュのクリア
            self._cache.clear()
            self._cache_timestamps.clear()
            
            # 参照のクリア
            self._main_window = None
            self._db = None
            
            # 最終クリーンアップ
            gc.collect()
            
            self.logger.info("終了処理完了")
            
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
        if not self._is_updating and self._last_group_id:
            self.schedule_update()
