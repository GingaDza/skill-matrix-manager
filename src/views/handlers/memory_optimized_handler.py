from PyQt6.QtCore import QObject, QTimer
from PyQt6.QtWidgets import QWidget
import logging
import psutil
import gc
import objgraph
from typing import Optional, Any, Dict, List
import weakref
import os

class MemoryOptimizedHandler(QObject):
    """メモリ最適化ハンドラー"""
    
    def __init__(self, db, main_window):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        # 弱参照の設定
        self._db = weakref.proxy(db)
        self._main_window = weakref.proxy(main_window)
        
        # メモリ管理用の設定
        self._cleanup_timer = QTimer(self)
        self._cleanup_timer.timeout.connect(self._check_memory_usage)
        
        # クリーンアップの閾値とタイミングを設定
        self._memory_threshold_mb = 100  # メモリ使用量の閾値（MB）
        self._cleanup_interval_ms = 30000  # クリーンアップの間隔（30秒）
        self._vms_threshold_mb = 1024  # VMS閾値（1GB）
        
        # オブジェクト監視
        self._object_counts: Dict[str, int] = {}
        self._widgets: List[weakref.ref] = []
        
        # ガベージコレクションの設定
        gc.enable()
        gc.set_debug(gc.DEBUG_STATS | gc.DEBUG_LEAK)
        gc.set_threshold(100, 5, 5)
        
        # クリーンアップタイマーの開始
        self._cleanup_timer.start(self._cleanup_interval_ms)
        
        self.logger.debug("MemoryOptimizedHandler initialized")
        self._log_memory_stats()

    def track_widget(self, widget: QWidget):
        """ウィジェットの追跡"""
        self._widgets.append(weakref.ref(widget))

    def _log_memory_stats(self):
        """メモリ統計情報のログ出力"""
        try:
            process = psutil.Process(os.getpid())
            
            # メモリ情報
            self.logger.debug("=== Memory Statistics ===")
            mem = process.memory_full_info()
            self.logger.debug(f"RSS: {mem.rss / (1024 * 1024):.1f}MB")
            self.logger.debug(f"VMS: {mem.vms / (1024 * 1024):.1f}MB")
            self.logger.debug(f"USS: {mem.uss / (1024 * 1024):.1f}MB")
            self.logger.debug(f"PSS: {mem.pss / (1024 * 1024):.1f}MB")
            
            # ガベージコレクション統計
            self.logger.debug("=== GC Statistics ===")
            for gen, count in enumerate(gc.get_count()):
                self.logger.debug(f"Generation {gen}: {count}")
            
            # オブジェクト統計
            stats = objgraph.typestats()
            growth = objgraph.show_growth()
            
            self.logger.debug("=== Object Growth ===")
            for name, growth_count in growth[:5]:  # Top 5
                self.logger.debug(f"{name}: +{growth_count}")
            
            # ウィジェット追跡
            live_widgets = [ref() for ref in self._widgets if ref() is not None]
            self.logger.debug(f"Live widgets: {len(live_widgets)}")
            
            self.logger.debug("========================")
            
        except Exception as e:
            self.logger.error(f"メモリ統計ログエラー: {e}")

    def _force_cleanup(self):
        """強制的なメモリクリーンアップ"""
        try:
            # ウィジェットのクリーンアップ
            for widget_ref in self._widgets[:]:
                widget = widget_ref()
                if widget is None:
                    self._widgets.remove(widget_ref)
                elif not widget.isVisible():
                    widget.deleteLater()
                    widget.setParent(None)
                    self._widgets.remove(widget_ref)
            
            # データベース接続のリセット
            if hasattr(self._db, 'reset_connections'):
                self._db.reset_connections()
            
            # ガベージコレクション
            for _ in range(3):  # 完全なクリーンアップのため複数回実行
                unreachable = gc.collect()
                if unreachable:
                    self.logger.warning(f"Unreachable objects: {unreachable}")
            
            # メモリ使用量の確認
            process = psutil.Process(os.getpid())
            mem = process.memory_full_info()
            
            if mem.vms > self._vms_threshold_mb * 1024 * 1024:
                self.logger.warning(
                    f"High VMS detected: {mem.vms / (1024*1024):.1f}MB"
                )
            
        except Exception as e:
            self.logger.error(f"クリーンアップエラー: {e}")

    def cleanup(self):
        """終了時のクリーンアップ"""
        self.logger.info("終了処理開始")
        
        try:
            # タイマーの停止
            if self._cleanup_timer and self._cleanup_timer.isActive():
                self._cleanup_timer.stop()
            
            # ウィジェットの解放
            for widget_ref in self._widgets[:]:
                widget = widget_ref()
                if widget is not None:
                    widget.deleteLater()
                    widget.setParent(None)
            self._widgets.clear()
            
            # リソースの解放
            self._db = None
            self._main_window = None
            self._cleanup_timer.deleteLater()
            self._cleanup_timer = None
            self._object_counts.clear()
            
            # 最終クリーンアップ
            self._force_cleanup()
            self._log_memory_stats()
            
            self.logger.info("終了処理完了")
            
        except Exception as e:
            self.logger.error(f"終了処理エラー: {e}")

    def _check_memory_usage(self, force: bool = False):
        """メモリ使用量のチェックとクリーンアップ"""
        try:
            process = psutil.Process()
            mem = process.memory_full_info()
            
            rss_mb = mem.rss / (1024 * 1024)
            vms_mb = mem.vms / (1024 * 1024)
            uss_mb = mem.uss / (1024 * 1024)
            
            self.logger.debug(
                f"Memory Usage - RSS: {rss_mb:.1f}MB, "
                f"VMS: {vms_mb:.1f}MB, "
                f"USS: {uss_mb:.1f}MB"
            )
            
            if (force or 
                rss_mb > self._memory_threshold_mb or 
                vms_mb > self._vms_threshold_mb):
                self.logger.info("強制クリーンアップ開始")
                self._force_cleanup()
                self._log_memory_stats()
                self.logger.info("強制クリーンアップ完了")
                
        except Exception as e:
            self.logger.error(f"メモリチェックエラー: {e}")
