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

    def _setup_timers(self):
        """タイマーの初期化"""
        # 更新スケジューラ
        self._update_timer = QTimer(self)
        self._update_timer.setSingleShot(True)
        self._update_timer.timeout.connect(self._process_update)
        
        # メモリ監視
        self._memory_timer = QTimer(self)
        self._memory_timer.timeout.connect(self._check_memory)
        self._memory_timer.start(2000)  # 2秒ごとにチェック
        
        # 自動クリーンアップ
        self._cleanup_timer = QTimer(self)
        self._cleanup_timer.timeout.connect(self._auto_cleanup)
        self._cleanup_timer.start(5000)  # 5秒ごとにクリーンアップ

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
        
        self._initial_memory = self._get_memory_usage()
        self._log_state("初期化")

    def _get_memory_usage(self) -> Dict[str, float]:
        """メモリ使用状況の取得"""
        try:
            process = psutil.Process()
            info = process.memory_info()
            return {
                'rss': info.rss / (1024 * 1024),
                'vms': info.vms / (1024 * 1024)
            }
        except Exception as e:
            self.logger.error(f"メモリ情報取得エラー: {e}")
            return {'rss': 0.0, 'vms': 0.0}

    def _log_state(self, action: str):
        """状態のログ記録"""
        try:
            mem = self._get_memory_usage()
            diff = {k: mem[k] - self._initial_memory[k] for k in mem}
            
            self.logger.debug(
                f"State ({action}):\n"
                f"  RSS: {mem['rss']:.1f}MB (Δ{diff['rss']:+.1f}MB)\n"
                f"  VMS: {mem['vms']:.1f}MB (Δ{diff['vms']:+.1f}MB)\n"
                f"  Workers: {len(self._workers)}\n"
                f"  Cache: {len(self._cache)}\n"
                f"  Updates: {self._update_count}"
            )
        except Exception as e:
            self.logger.error(f"状態ログ記録エラー: {e}")

    def _check_memory(self):
        """メモリ使用状況のチェック"""
        try:
            mem = self._get_memory_usage()
            if mem['rss'] > 150:  # 150MB超過で緊急クリーンアップ
                self._force_cleanup()
        except Exception as e:
            self.logger.error(f"メモリチェックエラー: {e}")

    def _force_cleanup(self):
        """強制メモリクリーンアップ"""
        try:
            self.logger.info("強制クリーンアップ開始")
            
            # キャッシュクリア
            self._cache.clear()
            
            # 完了した非同期処理のクリーンアップ
            self._workers = [w for w in self._workers if w.isRunning()]
            
            # 明示的なGC
            gc.collect()
            
            self._log_state("強制クリーンアップ完了")
            
        except Exception as e:
            self.logger.error(f"強制クリーンアップエラー: {e}")

    def _auto_cleanup(self):
        """定期的なクリーンアップ"""
        try:
            # 完了したワーカーの削除
            self._workers = [w for w in self._workers if w.isRunning()]
            
            # 古いキャッシュの削除
            if len(self._cache) > 100:
                self._cache.clear()
                
            gc.collect()
            
        except Exception as e:
            self.logger.error(f"自動クリーンアップエラー: {e}")

    @pyqtSlot()
    def _process_update(self):
        """更新処理の実行"""
        if self.is_updating:
            return

        try:
            self.is_updating = True
            self.update_started.emit()
            
            worker = UpdateWorker(self.db, self._last_group_id)
            worker.update_completed.connect(self._handle_update_completed)
            worker.error_occurred.connect(self._handle_update_error)
            worker.finished.connect(worker.deleteLater)
            
            self._workers.append(worker)
            worker.start()
            
        except Exception as e:
            self.logger.error(f"更新処理エラー: {e}")
            self.is_updating = False
            self._show_error("データ更新エラー")

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
            
        except Exception as e:
            self.logger.error(f"更新完了処理エラー: {e}")
        finally:
            self.is_updating = False
            self.update_finished.emit()
            self._log_state("更新完了")

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
            self._log_state("更新スケジュール")
            
        except Exception as e:
            self.logger.error(f"更新スケジュールエラー: {e}")

    def cleanup(self):
        """終了時のクリーンアップ"""
        try:
            self._log_state("終了処理開始")
            
            # タイマーの停止
            for timer in [self._update_timer, self._memory_timer, self._cleanup_timer]:
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
            
            gc.collect()
            self._log_state("終了処理完了")
            
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
