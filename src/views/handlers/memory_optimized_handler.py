from PyQt6.QtCore import QObject, QTimer, Qt
from PyQt6.QtWidgets import QWidget, QApplication
import logging
import psutil
import gc
import objgraph
import sys
from typing import Optional, Any, Dict, List, Set
import weakref
import os
import threading

class MemoryOptimizedHandler(QObject):
    """メモリ最適化ハンドラー"""
    
    def __init__(self, db, main_window):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        # メインスレッドの確認
        if not isinstance(threading.current_thread(), threading._MainThread):
            raise RuntimeError("MemoryOptimizedHandlerはメインスレッドで初期化する必要があります")
        
        # 弱参照の設定
        self._db = weakref.proxy(db)
        self._main_window = weakref.proxy(main_window)
        
        # メモリ管理用の設定
        self._cleanup_timer = QTimer(self)
        self._cleanup_timer.timeout.connect(self._check_memory_usage)
        
        # クリーンアップの閾値とタイミングを設定
        self._memory_threshold_mb = 100
        self._cleanup_interval_ms = 10000  # 10秒
        self._vms_threshold_mb = 512  # 512MB
        
        # オブジェクト追跡
        self._tracked_objects: Dict[int, weakref.ref] = {}
        self._qt_objects: Set[int] = set()
        self._widgets: List[weakref.ref] = []
        
        # ガベージコレクションの設定
        gc.set_debug(gc.DEBUG_LEAK | gc.DEBUG_STATS)
        gc.set_threshold(700, 10, 5)  # Qtオブジェクト用に調整
        
        # 初期クリーンアップ
        self._initial_cleanup()
        
        # タイマー開始
        self._cleanup_timer.start(self._cleanup_interval_ms)
        
        self.logger.debug("MemoryOptimizedHandler initialized")
        self._log_memory_stats()

    def _initial_cleanup(self):
        """初期クリーンアップ"""
        try:
            # 不要なモジュールの解放
            for module in list(sys.modules.keys()):
                if module not in sys.modules:
                    continue
                if not module.startswith(('PyQt6', 'src', 'logging', 'weakref')):
                    del sys.modules[module]
            
            # 完全なガベージコレクション
            for _ in range(2):  # 複数回実行して確実に
                gc.collect()
            
            # メモリ使用量の初期値を記録
            process = psutil.Process()
            mem = process.memory_full_info()
            self._initial_rss = mem.rss
            self._initial_vms = mem.vms
            
        except Exception as e:
            self.logger.error(f"初期クリーンアップエラー: {e}")

    def _track_qt_object(self, obj: QObject):
        """Qtオブジェクトの追跡"""
        try:
            obj_id = id(obj)
            if obj_id not in self._qt_objects:
                self._qt_objects.add(obj_id)
                obj.destroyed.connect(lambda: self._qt_object_destroyed(obj_id))
                
        except Exception as e:
            self.logger.error(f"Qtオブジェクト追跡エラー: {e}")

    def _qt_object_destroyed(self, obj_id: int):
        """Qtオブジェクトの破棄時のコールバック"""
        try:
            self._qt_objects.discard(obj_id)
        except Exception as e:
            self.logger.error(f"Qtオブジェクト破棄エラー: {e}")

    def track_widget(self, widget: QWidget):
        """ウィジェットの追跡"""
        try:
            if not widget.parent():
                widget.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
            
            widget_ref = weakref.ref(widget, self._widget_collected)
            self._widgets.append(widget_ref)
            self._track_qt_object(widget)
            
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
            
            self.logger.debug("=== Memory Statistics ===")
            self.logger.debug(f"RSS: {mem.rss / (1024 * 1024):.1f}MB")
            self.logger.debug(f"VMS: {mem.vms / (1024 * 1024):.1f}MB")
            self.logger.debug(f"USS: {mem.uss / (1024 * 1024):.1f}MB")
            
            if hasattr(self, '_initial_rss'):
                rss_diff = (mem.rss - self._initial_rss) / (1024 * 1024)
                vms_diff = (mem.vms - self._initial_vms) / (1024 * 1024)
                self.logger.debug(f"RSS変化: {rss_diff:+.1f}MB")
                self.logger.debug(f"VMS変化: {vms_diff:+.1f}MB")
            
            self.logger.debug("=== Qt Objects ===")
            self.logger.debug(f"追跡中のQtオブジェクト: {len(self._qt_objects)}")
            self.logger.debug(f"生存ウィジェット: {len(self._widgets)}")
            
            # GC統計
            gc_counts = gc.get_count()
            gc_thresholds = gc.get_threshold()
            self.logger.debug("=== GC Statistics ===")
            for i, (count, threshold) in enumerate(zip(gc_counts, gc_thresholds)):
                self.logger.debug(f"Generation {i}: {count}/{threshold}")
            
            # 未回収オブジェクト
            unreachable = gc.collect()
            if unreachable > 0:
                self.logger.warning(f"未回収オブジェクト: {unreachable}")
            
        except Exception as e:
            self.logger.error(f"メモリ統計ログエラー: {e}")

    def _force_cleanup(self):
        """強制的なメモリクリーンアップ"""
        try:
            # Qtオブジェクトの解放
            app = QApplication.instance()
            if app:
                app.processEvents()
            
            # ウィジェットの解放
            for widget_ref in self._widgets[:]:
                widget = widget_ref()
                if widget is None:
                    self._widgets.remove(widget_ref)
                elif not widget.isVisible():
                    if widget.parent() is None:
                        widget.deleteLater()
                    self._widgets.remove(widget_ref)
            
            # データベース接続のリセット
            if hasattr(self._db, 'reset_connections'):
                self._db.reset_connections()
            
            # 完全なガベージコレクション
            collected = 0
            for gen in range(2, -1, -1):
                collected += gc.collect(gen)
            
            if collected > 0:
                self.logger.info(f"解放されたオブジェクト: {collected}")
            
            # メモリ使用量の確認
            process = psutil.Process()
            mem = process.memory_full_info()
            
            if hasattr(self, '_initial_vms'):
                vms_increase = (mem.vms - self._initial_vms) / (1024 * 1024)
                if vms_increase > self._vms_threshold_mb:
                    self.logger.warning(
                        f"高メモリ使用量: VMS +{vms_increase:.1f}MB"
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
            
            # Qtオブジェクトの解放
            for obj_id in list(self._qt_objects):
                try:
                    obj = QObject.findChild(QObject, str(obj_id))
                    if obj:
                        obj.deleteLater()
                except:
                    pass
            self._qt_objects.clear()
            
            # ウィジェットの解放
            for widget_ref in self._widgets[:]:
                widget = widget_ref()
                if widget is not None:
                    widget.hide()
                    widget.setParent(None)
                    widget.deleteLater()
            self._widgets.clear()
            
            # リソースの解放
            self._db = None
            self._main_window = None
            self._cleanup_timer.deleteLater()
            self._cleanup_timer = None
            
            # 最終クリーンアップ
            self._force_cleanup()
            self._log_memory_stats()
            
            # 不要なモジュールの解放
            for module in list(sys.modules.keys()):
                if module not in sys.modules:
                    continue
                if not module.startswith(('PyQt6', 'src', 'logging')):
                    del sys.modules[module]
            
            # 最終的なガベージコレクション
            gc.collect()
            
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
