from PyQt6.QtCore import QObject, QTimer
import logging
import psutil
import gc
import objgraph
from typing import Optional, Any, Dict
import weakref
import os

class MemoryOptimizedHandler(QObject):
    """メモリ最適化ハンドラー"""
    
    def __init__(self, db, main_window):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        # 強参照を避けるため、弱参照を使用
        self._db = weakref.proxy(db)
        self._main_window = weakref.proxy(main_window)
        
        # メモリ管理用の設定
        self._cleanup_timer = QTimer()
        self._cleanup_timer.timeout.connect(self._check_memory_usage)
        
        # クリーンアップの閾値とタイミングを設定
        self._memory_threshold_mb = 100  # メモリ使用量の閾値（MB）
        self._cleanup_interval_ms = 10000  # クリーンアップの間隔（10秒）
        self._vms_threshold_mb = 1024  # VMS閾値（1GB）
        
        # オブジェクトカウント用の辞書
        self._object_counts: Dict[str, int] = {}
        
        # ガベージコレクションの設定
        gc.enable()
        gc.set_threshold(100, 5, 5)  # GCの閾値を調整
        
        # クリーンアップタイマーの開始
        self._cleanup_timer.start(self._cleanup_interval_ms)
        
        self.logger.debug("MemoryOptimizedHandler initialized")
        self._log_detailed_memory_info()

    def _log_detailed_memory_info(self):
        """詳細なメモリ情報のログ出力"""
        try:
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            
            self.logger.debug("=== Detailed Memory Information ===")
            self.logger.debug(f"RSS: {memory_info.rss / (1024 * 1024):.1f}MB")
            self.logger.debug(f"VMS: {memory_info.vms / (1024 * 1024):.1f}MB")
            self.logger.debug(f"Shared: {memory_info.shared / (1024 * 1024):.1f}MB")
            self.logger.debug(f"Text: {memory_info.text / (1024 * 1024):.1f}MB")
            self.logger.debug(f"Data: {memory_info.data / (1024 * 1024):.1f}MB")
            
            # オブジェクトの統計
            stats = objgraph.typestats()
            top_types = sorted(stats.items(), key=lambda x: x[1], reverse=True)[:10]
            
            self.logger.debug("=== Top 10 Object Types ===")
            for type_name, count in top_types:
                self.logger.debug(f"{type_name}: {count}")
            
            self.logger.debug("==============================")
            
        except Exception as e:
            self.logger.error(f"メモリ情報ログエラー: {e}")

    def load_initial_data(self):
        """初期データの読み込み"""
        self.logger.debug("初期データ読み込み開始")
        self._log_detailed_memory_info()
        
        try:
            self._check_memory_usage(force=True)
            
        except Exception as e:
            self.logger.error(f"初期データ読み込みエラー: {e}")
            raise

    def refresh_data(self):
        """データの更新"""
        self.logger.debug("データ更新リクエスト受信")
        
        try:
            self._check_memory_usage(force=True)
            
        except Exception as e:
            self.logger.error(f"データ更新エラー: {e}")

    def refresh_user_list(self):
        """ユーザーリストの更新"""
        self.logger.debug("ユーザーリスト更新リクエスト受信")
        
        try:
            self._check_memory_usage(force=True)
            
        except Exception as e:
            self.logger.error(f"ユーザーリスト更新エラー: {e}")

    def _check_memory_usage(self, force: bool = False):
        """メモリ使用量のチェックとクリーンアップ"""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            
            rss_mb = memory_info.rss / (1024 * 1024)
            vms_mb = memory_info.vms / (1024 * 1024)
            
            self.logger.debug(
                f"Memory Usage - RSS: {rss_mb:.1f}MB, "
                f"VMS: {vms_mb:.1f}MB"
            )
            
            # メモリ使用量が閾値を超えているか、強制クリーンアップの場合
            if force or rss_mb > self._memory_threshold_mb or vms_mb > self._vms_threshold_mb:
                self.logger.info("強制クリーンアップ開始")
                self._force_cleanup()
                self._log_detailed_memory_info()
                self.logger.info("強制クリーンアップ完了")
                
        except Exception as e:
            self.logger.error(f"メモリチェックエラー: {e}")

    def _force_cleanup(self):
        """強制的なメモリクリーンアップ"""
        try:
            # 不要なオブジェクトの解放
            for _ in range(3):  # 複数回実行して確実に解放
                gc.collect()
            
            # オブジェクトの追跡（デバッグ用）
            if self.logger.getEffectiveLevel() <= logging.DEBUG:
                stats = objgraph.typestats()
                current_counts = dict(sorted(
                    stats.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10])
                
                # 前回のカウントと比較
                if self._object_counts:
                    for type_name, count in current_counts.items():
                        prev_count = self._object_counts.get(type_name, 0)
                        if count > prev_count:
                            self.logger.warning(
                                f"オブジェクト増加: {type_name} "
                                f"({prev_count} -> {count})"
                            )
                
                self._object_counts = current_counts
            
        except Exception as e:
            self.logger.error(f"クリーンアップエラー: {e}")

    def cleanup(self):
        """終了時のクリーンアップ"""
        self.logger.info("終了処理開始")
        
        try:
            # タイマーの停止
            if self._cleanup_timer.isActive():
                self._cleanup_timer.stop()
            
            # 最終クリーンアップ
            self._force_cleanup()
            self._log_detailed_memory_info()
            
            # 参照のクリア
            self._db = None
            self._main_window = None
            self._cleanup_timer = None
            self._object_counts.clear()
            
            # 最終的なガベージコレクション
            gc.collect()
            
            self.logger.info("終了処理完了")
            
        except Exception as e:
            self.logger.error(f"終了処理エラー: {e}")
