import gc
import sys
import psutil
import threading
import tracemalloc
import logging
from typing import Dict, Set, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from weakref import WeakSet
from PyQt6.QtCore import QObject, QTimer
from contextlib import contextmanager

@dataclass
class MemorySnapshot:
    """メモリスナップショットデータ"""
    timestamp: datetime
    rss: float
    vms: float
    shared: float
    objects: int
    blocks: int
    refs: int

class ObjectTracker:
    """オブジェクトライフサイクル追跡"""
    
    def __init__(self):
        self._tracked: WeakSet = WeakSet()
        self._counts: Dict[str, int] = {}
        self._types: Dict[str, Set[int]] = {}
        self._creation_times: Dict[int, datetime] = {}
        
    def track(self, obj: Any, source: str = "unknown"):
        """オブジェクトの追跡開始"""
        obj_id = id(obj)
        self._tracked.add(obj)
        self._counts[source] = self._counts.get(source, 0) + 1
        
        obj_type = type(obj).__name__
        if obj_type not in self._types:
            self._types[obj_type] = set()
        self._types[obj_type].add(obj_id)
        
        self._creation_times[obj_id] = datetime.now()
        
    def untrack(self, obj: Any, source: str = "unknown"):
        """オブジェクトの追跡終了"""
        obj_id = id(obj)
        if obj in self._tracked:
            self._tracked.remove(obj)
            self._counts[source] = max(0, self._counts.get(source, 0) - 1)
            
            obj_type = type(obj).__name__
            if obj_type in self._types:
                self._types[obj_type].discard(obj_id)
            
            self._creation_times.pop(obj_id, None)
            
    def get_stats(self) -> Dict[str, Any]:
        """追跡統計の取得"""
        current_time = datetime.now()
        return {
            'total_objects': len(self._tracked),
            'source_counts': dict(self._counts),
            'type_counts': {
                t: len(ids) for t, ids in self._types.items()
            },
            'age_stats': {
                'oldest': max(
                    (current_time - t).total_seconds()
                    for t in self._creation_times.values()
                ) if self._creation_times else 0,
                'newest': min(
                    (current_time - t).total_seconds()
                    for t in self._creation_times.values()
                ) if self._creation_times else 0
            }
        }
        
    def cleanup(self):
        """トラッカーのクリーンアップ"""
        self._tracked.clear()
        self._counts.clear()
        self._types.clear()
        self._creation_times.clear()

class MemoryMonitor(QObject):
    """メモリ使用状況の監視"""
    
    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        
        # 監視設定
        self._monitoring = False
        self._snapshots: List[MemorySnapshot] = []
        self._max_snapshots = 100
        self._check_interval = 2000  # 2秒
        
        # トラッカー
        self._object_tracker = ObjectTracker()
        
        # 制限値
        self.limits = {
            'rss': 100,    # MB
            'vms': 350,    # MB
            'objects': 1000
        }
        
        # タイマー設定
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._check_memory)
        
        # トレースマロック
        tracemalloc.start()
        self._initial_snapshot = tracemalloc.take_snapshot()

    def start_monitoring(self):
        """監視の開始"""
        if not self._monitoring:
            self._monitoring = True
            self._timer.start(self._check_interval)
            self.logger.info("メモリ監視を開始しました")

    def stop_monitoring(self):
        """監視の停止"""
        if self._monitoring:
            self._monitoring = False
            self._timer.stop()
            self.logger.info("メモリ監視を停止しました")

    def _check_memory(self):
        """メモリ使用状況のチェック"""
        try:
            snapshot = self._take_snapshot()
            self._analyze_snapshot(snapshot)
            
            # 制限チェック
            if self._check_limits(snapshot):
                self._handle_limit_exceeded()
                
        except Exception as e:
            self.logger.error(f"メモリチェックエラー: {e}")

    def _take_snapshot(self) -> MemorySnapshot:
        """メモリスナップショットの取得"""
        try:
            process = psutil.Process()
            mem = process.memory_info()
            
            snapshot = MemorySnapshot(
                timestamp=datetime.now(),
                rss=mem.rss / (1024 * 1024),
                vms=mem.vms / (1024 * 1024),
                shared=getattr(mem, 'shared', 0) / (1024 * 1024),
                objects=len(gc.get_objects()),
                blocks=len(tracemalloc.get_traced_memory()),
                refs=len(gc.get_referrers(*gc.get_objects()))
            )
            
            self._snapshots.append(snapshot)
            if len(self._snapshots) > self._max_snapshots:
                self._snapshots.pop(0)
                
            return snapshot
            
        except Exception as e:
            self.logger.error(f"スナップショット取得エラー: {e}")
            raise

    def _analyze_snapshot(self, snapshot: MemorySnapshot):
        """スナップショットの分析"""
        try:
            # メモリ使用傾向の分析
            if len(self._snapshots) > 1:
                prev = self._snapshots[-2]
                time_diff = (snapshot.timestamp - prev.timestamp).total_seconds()
                
                rss_rate = (snapshot.rss - prev.rss) / time_diff
                vms_rate = (snapshot.vms - prev.vms) / time_diff
                obj_rate = (snapshot.objects - prev.objects) / time_diff
                
                self.logger.debug(
                    f"メモリ使用傾向:\n"
                    f"RSS変化率: {rss_rate:.2f}MB/s\n"
                    f"VMS変化率: {vms_rate:.2f}MB/s\n"
                    f"オブジェクト変化率: {obj_rate:.2f}個/s"
                )
            
            # トレースマロック分析
            current = tracemalloc.take_snapshot()
            diff = current.compare_to(self._initial_snapshot, 'lineno')
            
            self.logger.debug("\nメモリブロック上位10件:")
            for stat in diff[:10]:
                self.logger.debug(f"{stat}")
                
        except Exception as e:
            self.logger.error(f"スナップショット分析エラー: {e}")

    def _check_limits(self, snapshot: MemorySnapshot) -> bool:
        """制限値のチェック"""
        return (
            snapshot.rss > self.limits['rss'] or
            snapshot.vms > self.limits['vms'] or
            snapshot.objects > self.limits['objects']
        )

    def _handle_limit_exceeded(self):
        """制限超過時の処理"""
        self.logger.warning("メモリ制限を超過しました")
        self.force_cleanup()

    @contextmanager
    def track_operation(self, operation_name: str):
        """操作のメモリ追跡"""
        start_snapshot = self._take_snapshot()
        start_time = datetime.now()
        
        try:
            yield
        finally:
            end_snapshot = self._take_snapshot()
            duration = (datetime.now() - start_time).total_seconds()
            
            self.logger.info(
                f"\n操作メモリ分析: {operation_name}\n"
                f"実行時間: {duration:.2f}秒\n"
                f"RSS変化: {end_snapshot.rss - start_snapshot.rss:.1f}MB\n"
                f"VMS変化: {end_snapshot.vms - start_snapshot.vms:.1f}MB\n"
                f"オブジェクト変化: {end_snapshot.objects - start_snapshot.objects}"
            )

    def track_object(self, obj: Any, source: str = "unknown"):
        """オブジェクトの追跡"""
        self._object_tracker.track(obj, source)

    def untrack_object(self, obj: Any, source: str = "unknown"):
        """オブジェクトの追跡解除"""
        self._object_tracker.untrack(obj, source)

    def get_object_stats(self) -> Dict[str, Any]:
        """オブジェクト統計の取得"""
        return self._object_tracker.get_stats()

    def force_cleanup(self):
        """強制クリーンアップ"""
        self.logger.info("強制クリーンアップを開始")
        
        # 明示的なGC
        gc.collect()
        gc.collect()
        
        # スナップショットのクリア
        if len(self._snapshots) > 10:
            self._snapshots = self._snapshots[-10:]
            
        # トレースマロックのリセット
        tracemalloc.clear_traces()
        
        self.logger.info("強制クリーンアップ完了")

    def cleanup(self):
        """終了時のクリーンアップ"""
        self.stop_monitoring()
        self._object_tracker.cleanup()
        self._snapshots.clear()
        tracemalloc.stop()
        gc.collect()
        gc.collect()

