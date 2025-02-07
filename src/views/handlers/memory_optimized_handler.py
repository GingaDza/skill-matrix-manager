from PyQt6.QtCore import QObject, QTimer
from PyQt6.QtWidgets import QWidget
import logging
import psutil
import gc
import objgraph
import sys
from typing import Optional, Any, Dict, List, Set
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
        self._memory_threshold_mb = 100
        self._cleanup_interval_ms = 15000  # 15秒
        self._vms_threshold_mb = 512  # 512MB
        
        # オブジェクト追跡
        self._tracked_objects: Set[int] = set()
        self._widgets: List[weakref.ref] = []
        self._last_unreachable = 0
        
        # ガベージコレクションの設定
        gc.set_debug(gc.DEBUG_LEAK | gc.DEBUG_STATS)
        gc.set_threshold(100, 10, 10)
        
        # 初期クリーンアップ
        self._initial_cleanup()
        
        # タイマー開始
        self._cleanup_timer.start(self._cleanup_interval_ms)
        
        self.logger.debug("MemoryOptimizedHandler initialized")
        self._log_memory_stats()

    def _initial_cleanup(self):
        """初期クリーンアップ"""
        try:
            # 未使用モジュールの解放
            for module in list(sys.modules.keys()):
                if module not in sys.modules:
                    continue
                if not module.startswith(('PyQt6', 'src')):
                    del sys.modules[module]
            
            # 完全なガベージコレクション
            gc.collect(2)
            
            # メモリ使用量の初期値を記録
            process = psutil.Process()
            mem = process.memory_full_info()
            self._initial_rss = mem.rss
            self._initial_vms = mem.vms
            
        except Exception as e:
            self.logger.error(f"初期クリーンアップエラー: {e}")

    def _track_object(self, obj: Any):
        """オブジェクトの追跡"""
        if not hasattr(obj, '__dict__'):
            return
        
        obj_id = id(obj)
        if obj_id not in self._tracked_objects:
            self._tracked_objects.add(obj_id)
            weakref.finalize(obj, self._object_finalized, obj_id)

    def _object_finalized(self, obj_id: int):
        """オブジェクトの終了処理"""
        try:
            self._tracked_objects.discard(obj_id)
        except Exception as e:
            self.logger.error(f"オブジェクト終了処理エラー: {e}")

    def track_widget(self, widget: QWidget):
        """ウィジェットの追跡"""
        try:
            widget_ref = weakref.ref(widget, self._widget_collected)
            self._widgets.append(widget_ref)
            self._track_object(widget)
            
        except Exception as e:
            self.logger.error(f"ウィジェット追跡エラー: {e}")

    def _widget_collected(self, ref):
        """ウィジェット解放時のコールバック"""
        try:
            self._widgets.remove(ref)
        except ValueError:
            pass

    def _log_memory_stats(self):
        """メモリ統計情報のログ出力"""
        try:
            process = psutil.Process()
            mem = process.memory_full_info()
            
            # メモリ使用量
            rss_mb = mem.rss / (1024 * 1024)
            vms_mb = mem.vms / (1024 * 1024)
            uss_mb = mem.uss / (1024 * 1024)
            
            self.logger.debug("=== Memory Statistics ===")
            self.logger.debug(f"RSS: {rss_mb:.1f}MB")
            self.logger.debug(f"VMS: {vms_mb:.1f}MB")
            self.logger.debug(f"USS: {uss_mb:.1f}MB")
            
            # 初期値との比較
            if hasattr(self, '_initial_rss'):
                rss_diff = (mem.rss - self._initial_rss) / (1024 * 1024)
                vms_diff = (mem.vms - self._initial_vms) / (1024 * 1024)
                self.logger.debug(f"RSS変化: {rss_diff:+.1f}MB")
                self.logger.debug(f"VMS変化: {vms_diff:+.1f}MB")
            
            # GC統計
            self.logger.debug("=== GC Statistics ===")
            counts = gc.get_count()
            for gen, count in enumerate(counts):
                threshold = gc.get_threshold()[gen]
                self.logger.debug(f"Gen {gen}: {count}/{threshold}")
            
            # オブジェクト統計
            self.logger.debug("=== Object Statistics ===")
            self.logger.debug(f"追跡オブジェクト: {len(self._tracked_objects)}")
            self.logger.debug(f"生存ウィジェット: {len(self._widgets)}")
            
            # 未回収オブジェクト
            unreachable = gc.collect()
            if unreachable != self._last_unreachable:
                self.logger.warning(f"未回収オブジェクト: {unreachable}")
                self._last_unreachable = unreachable
            
        except Exception as e:
            self.logger.error(f"メモリ統計ログエラー: {e}")

    def _force_cleanup(self):
        """強制的なメモリクリーンアップ"""
        try:
            # 参照カウントが0のウィジェットを解放
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
            
            # 完全なガベージコレクション
            for gen in range(2, -1, -1):
                unreachable = gc.collect(gen)
                if unreachable:
                    self.logger.warning(f"Gen {gen}で未回収: {unreachable}")
            
            # メモリ使用量の確認
            process = psutil.Process()
            mem = process.memory_full_info()
            
            # 異常な増加をチェック
            if hasattr(self, '_initial_vms'):
                vms_increase = (mem.vms - self._initial_vms) / (1024 * 1024)
                if vms_increase > self._vms_threshold_mb:
                    self.logger.error(
                        f"異常なVMS増加: +{vms_increase:.1f}MB"
                    )
            
        except Exception as e:
            self.logger.error(f"クリーンアップエラー: {e}")

    def cleanup(self):
        """終了時のクリーンアップ"""
        self.logger.info("終了処理開始")
        
        try:
            # タイマーの停止
            if self._cleanup_timer.isActive():
                self._cleanup_timer.stop()
            
            # ウィジェットの解放
            for widget_ref in self._widgets[:]:
                widget = widget_ref()
                if widget is not None:
                    widget.hide()
                    widget.deleteLater()
                    widget.setParent(None)
            self._widgets.clear()
            
            # 追跡オブジェクトのクリア
            self._tracked_objects.clear()
            
            # リソースの解放
            self._db = None
            self._main_window = None
            self._cleanup_timer.deleteLater()
            self._cleanup_timer = None
            
            # 最終クリーンアップ
            self._force_cleanup()
            self._log_memory_stats()
            
            # モジュールのクリーンアップ
            for module in list(sys.modules.keys()):
                if module not in sys.modules:
                    continue
                if not module.startswith(('PyQt6', 'src')):
                    del sys.modules[module]
            
            self.logger.info("終了処理完了")
            
        except Exception as e:
            self.logger.error(f"終了処理エラー: {e}")
            raise

    def _check_memory_usage(self, force: bool = False):
        """メモリ使用量のチェックとクリーンアップ"""
        try:
            process = psutil.Process()
            mem = process.memory_full_info()
            
            rss_mb = mem.rss / (1024 * 1024)
            vms_mb = mem.vms / (1024 * 1024)
            
            self.logger.debug(
                f"Memory Usage - RSS: {rss_mb:.1f}MB, "
                f"VMS: {vms_mb:.1f}MB"
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
