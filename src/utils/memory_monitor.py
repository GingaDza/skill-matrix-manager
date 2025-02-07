import gc
import sys
import psutil
import threading
import tracemalloc
import logging
from typing import Dict, Set, Any, Optional, List, Tuple
from datetime import datetime
from dataclasses import dataclass
from contextlib import contextmanager
from PyQt6.QtCore import QObject, QTimer

@dataclass
class MemoryStats:
    """メモリ統計情報"""
    rss: float
    vms: float
    shared: float
    private: float
    timestamp: datetime
    tracked_objects: int
    total_objects: int

class ReferenceTracker:
    """参照追跡管理"""
    def __init__(self):
        self._refs: Dict[int, Set[int]] = {}
        self._creation_times: Dict[int, datetime] = {}
        self._type_stats: Dict[str, int] = {}
        
    def track(self, obj: Any) -> None:
        """オブジェクトの参照を追跡"""
        obj_id = id(obj)
        if obj_id not in self._refs:
            self._refs[obj_id] = {
                id(ref) for ref in gc.get_referrers(obj)
                if hasattr(ref, '__class__')
            }
            self._creation_times[obj_id] = datetime.now()
            self._type_stats[type(obj).__name__] = \
                self._type_stats.get(type(obj).__name__, 0) + 1

    def untrack(self, obj: Any) -> None:
        """オブジェクトの追跡を解除"""
        obj_id = id(obj)
        if obj_id in self._refs:
            self._refs.pop(obj_id)
            self._creation_times.pop(obj_id)
            type_name = type(obj).__name__
            self._type_stats[type_name] = \
                max(0, self._type_stats.get(type_name, 0) - 1)

    def get_stats(self) -> Dict[str, Any]:
        """参照統計を取得"""
        now = datetime.now()
        return {
            'total_refs': sum(len(refs) for refs in self._refs.values()),
            'object_count': len(self._refs),
            'type_stats': dict(self._type_stats),
            'age_stats': {
                obj_id: (now - creation_time).total_seconds()
                for obj_id, creation_time in self._creation_times.items()
            }
        }

    def analyze_cycles(self) -> List[Tuple[int, ...]]:
        """循環参照を検出"""
        cycles = []
        visited = set()
        
        def find_cycle(obj_id: int, path: List[int]) -> Optional[List[int]]:
            if obj_id in path:
                cycle_start = path.index(obj_id)
                return path[cycle_start:]
            if obj_id in visited or obj_id not in self._refs:
                return None
                
            visited.add(obj_id)
            path.append(obj_id)
            
            for ref_id in self._refs[obj_id]:
                cycle = find_cycle(ref_id, path)
                if cycle:
                    return cycle
                    
            path.pop()
            return None

        for obj_id in list(self._refs.keys()):
            cycle = find_cycle(obj_id, [])
            if cycle:
                cycles.append(tuple(cycle))
                
        return cycles

    def cleanup(self) -> None:
        """トラッカーのクリーンアップ"""
        self._refs.clear()
        self._creation_times.clear()
        self._type_stats.clear()

class MemoryMonitor(QObject):
    """メモリ監視システム"""
    
    MEMORY_LIMITS = {
        'rss': 100.0,      # MB
        'vms': 350.0,      # MB
        'objects': 1000,
        'tracemalloc': 50  # スナップショット数
    }
    
    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        
        # トラッカーの初期化
        self._ref_tracker = ReferenceTracker()
        
        # 統計情報
        self._stats_history: List[MemoryStats] = []
        self._max_history = 100
        self._last_gc_count = 0
        
        # トレースマロック設定
        tracemalloc.start(25)  # スタックフレーム25まで追跡
        self._initial_snapshot = tracemalloc.take_snapshot()
        self._snapshots: List[Tuple[datetime, tracemalloc.Snapshot]] = []
        
        # タイマー設定
        self._setup_timers()
        
        # 初期メモリ使用量を記録
        self._record_stats()

    def _setup_timers(self) -> None:
        """タイマーの設定"""
        # メモリ統計タイマー
        self._stats_timer = QTimer(self)
        self._stats_timer.timeout.connect(self._record_stats)
        self._stats_timer.start(2000)  # 2秒間隔
        
        # クリーンアップタイマー
        self._cleanup_timer = QTimer(self)
        self._cleanup_timer.timeout.connect(self._auto_cleanup)
        self._cleanup_timer.start(30000)  # 30秒間隔

    def _record_stats(self) -> None:
        """メモリ統計の記録"""
        try:
            process = psutil.Process()
            mem = process.memory_info()
            
            stats = MemoryStats(
                rss=mem.rss / (1024 * 1024),
                vms=mem.vms / (1024 * 1024),
                shared=getattr(mem, 'shared', 0) / (1024 * 1024),
                private=getattr(mem, 'private', 0) / (1024 * 1024),
                timestamp=datetime.now(),
                tracked_objects=len(self._ref_tracker._refs),
                total_objects=len(gc.get_objects())
            )
            
            self._stats_history.append(stats)
            if len(self._stats_history) > self._max_history:
                self._stats_history.pop(0)
                
            # スナップショットの取得
            if len(self._snapshots) < self.MEMORY_LIMITS['tracemalloc']:
                snapshot = tracemalloc.take_snapshot()
                self._snapshots.append((datetime.now(), snapshot))
                
            # 制限チェック
            self._check_limits(stats)
            
            # GCの監視
            gc_count = gc.get_count()[0]
            if gc_count > self._last_gc_count + 10:
                self.logger.warning(f"GC頻度が高くなっています: {gc_count}")
                self._last_gc_count = gc_count
                
        except Exception as e:
            self.logger.error(f"統計記録エラー: {e}")

    def _check_limits(self, stats: MemoryStats) -> None:
        """メモリ制限のチェック"""
        if stats.rss > self.MEMORY_LIMITS['rss']:
            self.logger.warning(f"RSS制限超過: {stats.rss:.1f}MB")
            self.force_cleanup()
            
        if stats.vms > self.MEMORY_LIMITS['vms']:
            self.logger.warning(f"VMS制限超過: {stats.vms:.1f}MB")
            self.force_cleanup()
            
        if stats.total_objects > self.MEMORY_LIMITS['objects']:
            self.logger.warning(
                f"オブジェクト数制限超過: {stats.total_objects}"
            )
            self.force_cleanup()

    def _auto_cleanup(self) -> None:
        """自動クリーンアップ"""
        try:
            # 古いスナップショットの削除
            now = datetime.now()
            self._snapshots = [
                (t, s) for t, s in self._snapshots
                if (now - t).total_seconds() < 300  # 5分以内
            ]
            
            # 循環参照の検出と報告
            cycles = self._ref_tracker.analyze_cycles()
            if cycles:
                self.logger.warning(
                    f"循環参照を検出: {len(cycles)}個"
                )
                
            # 統計履歴の制限
            if len(self._stats_history) > self._max_history:
                self._stats_history = self._stats_history[-self._max_history:]
                
            gc.collect()
            
        except Exception as e:
            self.logger.error(f"自動クリーンアップエラー: {e}")

    def force_cleanup(self) -> None:
        """強制クリーンアップ"""
        try:
            self.logger.info("強制クリーンアップ開始")
            
            # スナップショットの分析
            if self._snapshots:
                latest = self._snapshots[-1][1]
                diff = latest.compare_to(self._initial_snapshot, 'lineno')
                
                self.logger.debug("\nメモリ増加の主な原因:")
                for stat in diff[:5]:
                    self.logger.debug(f"{stat}")
                    
            # 参照の分析
            stats = self._ref_tracker.get_stats()
            self.logger.debug(
                f"\n参照統計:\n"
                f"総参照数: {stats['total_refs']}\n"
                f"オブジェクト数: {stats['object_count']}\n"
                f"型別統計: {stats['type_stats']}"
            )
            
            # クリーンアップ実行
            self._ref_tracker.cleanup()
            gc.collect()
            gc.collect()
            
            self.logger.info("強制クリーンアップ完了")
            
        except Exception as e:
            self.logger.error(f"強制クリーンアップエラー: {e}")

    @contextmanager
    def track_operation(self, name: str):
        """操作のメモリ追跡"""
        start_stats = self._stats_history[-1] if self._stats_history else None
        start_time = datetime.now()
        
        try:
            yield
        finally:
            end_stats = self._stats_history[-1] if self._stats_history else None
            duration = (datetime.now() - start_time).total_seconds()
            
            if start_stats and end_stats:
                self.logger.info(
                    f"\n操作メモリ分析: {name}\n"
                    f"実行時間: {duration:.2f}秒\n"
                    f"RSS変化: {end_stats.rss - start_stats.rss:.1f}MB\n"
                    f"VMS変化: {end_stats.vms - start_stats.vms:.1f}MB\n"
                    f"オブジェクト変化: "
                    f"{end_stats.total_objects - start_stats.total_objects}"
                )

    def track_object(self, obj: Any) -> None:
        """オブジェクトの追跡"""
        self._ref_tracker.track(obj)

    def untrack_object(self, obj: Any) -> None:
        """オブジェクトの追跡解除"""
        self._ref_tracker.untrack(obj)

    def cleanup(self) -> None:
        """終了時のクリーンアップ"""
        try:
            self.logger.info("メモリモニター終了処理開始")
            
            # タイマー停止
            self._stats_timer.stop()
            self._cleanup_timer.stop()
            
            # トラッカーのクリーンアップ
            self._ref_tracker.cleanup()
            
            # 履歴クリア
            self._stats_history.clear()
            self._snapshots.clear()
            
            # トレースマロック停止
            tracemalloc.stop()
            
            gc.collect()
            gc.collect()
            
            self.logger.info("メモリモニター終了処理完了")
            
        except Exception as e:
            self.logger.error(f"メモリモニター終了処理エラー: {e}")


    def load_initial_data(self):
        """初期データの読み込み"""
        self.logger.debug("初期データ読み込み開始")
        with self._memory_monitor.track_operation("初期データ読み込み"):
            self.schedule_update(immediate=True)

    def refresh_data(self):
        """データの更新をリクエスト"""
        self.logger.debug("データ更新リクエスト受信")
        with self._memory_monitor.track_operation("データ更新"):
            self.schedule_update()

    def refresh_user_list(self):
        """ユーザーリストの更新をリクエスト"""
        self.logger.debug("ユーザーリスト更新リクエスト受信")
        if not self._is_updating and self._last_group_id:
            with self._memory_monitor.track_operation("ユーザーリスト更新"):
                self.schedule_update()
