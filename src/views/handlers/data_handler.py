[前のdata_handler.pyの内容を保持しながら、以下の変更を追加]

from src.utils.memory_tracker import MemoryTracker

class DataHandler(QObject):
    def __init__(self, db, main_window):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.memory_tracker = MemoryTracker()
        
        # ... [既存の初期化コード] ...
        
        self.memory_tracker.track_object(self, "DataHandler")
        self.memory_tracker.log_tracking_info("DataHandler初期化完了")

    def _setup_timers(self):
        """タイマーの初期化"""
        # ... [既存のタイマー設定コード] ...
        
        # メモリ監視タイマーの追加
        self._memory_check_timer = QTimer(self)
        self._memory_check_timer.timeout.connect(self._check_memory_detailed)
        self._memory_check_timer.start(1000)  # 1秒ごとにチェック

    def _check_memory_detailed(self):
        """詳細なメモリチェック"""
        try:
            self.memory_tracker.take_snapshot(f"定期チェック_{self._update_count}")
            self.memory_tracker.log_tracking_info("定期メモリチェック")
            
            # リーク検出
            if self._update_count % 10 == 0:  # 10回の更新ごとにリークチェック
                self.memory_tracker.check_leaks()
                
        except Exception as e:
            self.logger.error(f"詳細メモリチェックエラー: {e}")

    def _process_update(self):
        """更新処理の実行"""
        if self.is_updating:
            return

        try:
            self.is_updating = True
            self.update_started.emit()
            
            # 更新前のスナップショット
            self.memory_tracker.take_snapshot(f"更新開始_{self._update_count}")
            
            worker = UpdateWorker(self.db, self._last_group_id)
            self.memory_tracker.track_object(worker, "UpdateWorker")
            
            worker.update_completed.connect(self._handle_update_completed)
            worker.error_occurred.connect(self._handle_update_error)
            worker.finished.connect(lambda: self._cleanup_worker(worker))
            
            self._workers.append(worker)
            worker.start()
            
        except Exception as e:
            self.logger.error(f"更新処理エラー: {e}")
            self.is_updating = False
            self._show_error("データ更新エラー")

    def _cleanup_worker(self, worker):
        """ワーカーのクリーンアップ"""
        try:
            self.memory_tracker.untrack_object(worker, "UpdateWorker")
            worker.deleteLater()
            if worker in self._workers:
                self._workers.remove(worker)
        except Exception as e:
            self.logger.error(f"ワーカークリーンアップエラー: {e}")

    def cleanup(self):
        """終了時のクリーンアップ"""
        try:
            self.memory_tracker.log_tracking_info("終了処理開始")
            
            # ... [既存のクリーンアップコード] ...
            
            self.memory_tracker.cleanup()
            
        except Exception as e:
            self.logger.error(f"終了処理エラー: {e}")

