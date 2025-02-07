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
from src.utils.memory_tracker import MemoryTracker

class UpdateWorker(QThread):
    """非同期更新処理を行うワーカー"""
    update_completed = pyqtSignal(list, list)
    error_occurred = pyqtSignal(str)
    
    # キャッシュサイズを制限
    @lru_cache(maxsize=32)
    def _get_users(self, group_id: int) -> List[Tuple[int, str]]:
        return self.db.get_users_by_group(group_id)

    def __init__(self, db, group_id=None):
        super().__init__()
        self.db = db
        self.group_id = group_id
        self._cache: Dict[str, Any] = {}
        
    def run(self):
        try:
            groups = self.db.get_all_groups()
            users = []
            if self.group_id is not None:
                users = self._get_users(self.group_id)
            self.update_completed.emit(groups, users)
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self._cache.clear()

class DataHandler(QObject):
    """データ操作を管理するハンドラー"""
    update_started = pyqtSignal()
    update_finished = pyqtSignal()
    
    # メモリ制限値
    MEMORY_LIMITS = {
        'rss': 120,  # MB
        'vms': 350,  # MB
        'cleanup_threshold': 100  # MB
    }
    
    # 更新間隔
    UPDATE_INTERVALS = {
        'normal': 250,  # ms
        'memory_check': 2000,  # ms
        'cleanup': 5000,  # ms
    }

    def __init__(self, db, main_window):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.memory_tracker = MemoryTracker()
        
        # 基本設定
        self.db = db
        self._main_window = main_window
        self.is_updating = False
        
        # メモリ管理
        self._cached_data: Dict[str, Any] = {}
        self._active_workers: Set[QThread] = set()
        self._update_count = 0
        
        # 状態管理
        self._last_group_id = None
        self._last_user_id = None
        self._ui_state = {}
        
        # 初期化
        self._setup_timers()
        self._setup_debug()
        
        # トラッキング開始
        self.memory_tracker.track_object(self, "DataHandler")
        self.memory_tracker.log_tracking_info("DataHandler初期化完了")

    def _setup_timers(self):
        """タイマーの初期化"""
        # 更新タイマー（弱参照で管理）
        self._timers = {
            'update': QTimer(self),
            'memory': QTimer(self),
            'cleanup': QTimer(self)
        }
        
        # タイマー設定
        self._timers['update'].setSingleShot(True)
        self._timers['update'].timeout.connect(self._process_update)
        
        self._timers['memory'].timeout.connect(self._check_memory)
        self._timers['memory'].start(self.UPDATE_INTERVALS['memory_check'])
        
        self._timers['cleanup'].timeout.connect(self._auto_cleanup)
        self._timers['cleanup'].start(self.UPDATE_INTERVALS['cleanup'])
        
        # トラッキング
        for name, timer in self._timers.items():
            self.memory_tracker.track_object(timer, f"Timer_{name}")

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

    def _check_memory(self):
        """メモリ使用状況のチェック"""
        try:
            mem = self.memory_tracker.get_memory_usage()
            
            if mem.get('rss', 0) > self.MEMORY_LIMITS['rss']:
                self._force_cleanup()
            elif mem.get('rss', 0) > self.MEMORY_LIMITS['cleanup_threshold']:
                self._auto_cleanup()
                
            self.memory_tracker.take_snapshot(f"メモリチェック_{self._update_count}")
            
        except Exception as e:
            self.logger.error(f"メモリチェックエラー: {e}")

    def _force_cleanup(self):
        """強制メモリクリーンアップ"""
        try:
            self.logger.info("強制クリーンアップ開始")
            
            # キャッシュクリア
            self._cached_data.clear()
            
            # 完了したワーカーの削除
            self._cleanup_workers()
            
            # 明示的なGC
            gc.collect()
            
            self.memory_tracker.log_tracking_info("強制クリーンアップ完了")
            
        except Exception as e:
            self.logger.error(f"強制クリーンアップエラー: {e}")

    def _auto_cleanup(self):
        """定期的なクリーンアップ"""
        try:
            # 長時間キャッシュされたデータの削除
            current_time = datetime.now()
            self._cached_data = {
                k: v for k, v in self._cached_data.items()
                if (current_time - v.get('timestamp', current_time)).seconds < 300
            }
            
            self._cleanup_workers()
            gc.collect()
            
        except Exception as e:
            self.logger.error(f"自動クリーンアップエラー: {e}")

    def _cleanup_workers(self):
        """ワーカーのクリーンアップ"""
        try:
            completed_workers = {
                worker for worker in self._active_workers
                if not worker.isRunning()
            }
            
            for worker in completed_workers:
                self.memory_tracker.untrack_object(worker, "UpdateWorker")
                worker.deleteLater()
                self._active_workers.remove(worker)
                
        except Exception as e:
            self.logger.error(f"ワーカークリーンアップエラー: {e}")

[続く...]
