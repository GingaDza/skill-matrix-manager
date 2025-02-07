import gc
import sys
import psutil
import tracemalloc
import logging
from typing import Dict, Any, Set
from datetime import datetime
from weakref import WeakSet
from PyQt6.QtCore import QObject

class MemoryTracker:
    """メモリ使用状況とオブジェクトライフサイクルの追跡"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._start_time = datetime.now()
        self._tracked_objects = WeakSet()
        self._object_counts: Dict[str, int] = {}
        self._peak_memory = 0
        self._snapshots = []
        
        # トレースマロックの開始
        tracemalloc.start()
        self._initial_snapshot = tracemalloc.take_snapshot()

    def track_object(self, obj: QObject, source: str = "unknown"):
        """オブジェクトの追跡を開始"""
        self._tracked_objects.add(obj)
        self._object_counts[source] = self._object_counts.get(source, 0) + 1
        self.log_tracking_info(f"オブジェクト追加: {obj.__class__.__name__} from {source}")

    def untrack_object(self, obj: QObject, source: str = "unknown"):
        """オブジェクトの追跡を終了"""
        if obj in self._tracked_objects:
            self._tracked_objects.remove(obj)
            self._object_counts[source] = self._object_counts.get(source, 0) - 1
            self.log_tracking_info(f"オブジェクト削除: {obj.__class__.__name__} from {source}")

    def get_memory_usage(self) -> Dict[str, float]:
        """現在のメモリ使用状況を取得"""
        try:
            process = psutil.Process()
            mem_info = process.memory_info()
            current_usage = {
                'rss': mem_info.rss / (1024 * 1024),
                'vms': mem_info.vms / (1024 * 1024),
                'shared': getattr(mem_info, 'shared', 0) / (1024 * 1024),
                'text': getattr(mem_info, 'text', 0) / (1024 * 1024),
                'data': getattr(mem_info, 'data', 0) / (1024 * 1024)
            }
            
            # ピークメモリの更新
            self._peak_memory = max(self._peak_memory, current_usage['rss'])
            
            return current_usage
        except Exception as e:
            self.logger.error(f"メモリ使用状況取得エラー: {e}")
            return {}

    def take_snapshot(self, label: str):
        """メモリスナップショットの取得"""
        try:
            snapshot = tracemalloc.take_snapshot()
            self._snapshots.append((label, snapshot))
            diff = snapshot.compare_to(self._initial_snapshot, 'lineno')
            
            # 差分の上位10件を記録
            self.logger.debug(f"\nメモリスナップショット ({label}):")
            for stat in diff[:10]:
                self.logger.debug(f"{stat}")
                
        except Exception as e:
            self.logger.error(f"スナップショット取得エラー: {e}")

    def get_object_stats(self) -> Dict[str, Any]:
        """オブジェクト統計の取得"""
        stats = {
            'tracked_objects': len(self._tracked_objects),
            'object_counts': dict(self._object_counts),
            'gc_objects': len(gc.get_objects()),
            'peak_memory_mb': self._peak_memory,
            'uptime_seconds': (datetime.now() - self._start_time).total_seconds()
        }
        return stats

    def log_tracking_info(self, message: str):
        """トラッキング情報のログ出力"""
        try:
            mem_usage = self.get_memory_usage()
            stats = self.get_object_stats()
            
            self.logger.debug(
                f"\n=== メモリトラッキング情報 ===\n"
                f"メッセージ: {message}\n"
                f"RSS: {mem_usage.get('rss', 0):.1f}MB\n"
                f"VMS: {mem_usage.get('vms', 0):.1f}MB\n"
                f"共有メモリ: {mem_usage.get('shared', 0):.1f}MB\n"
                f"テキストセグメント: {mem_usage.get('text', 0):.1f}MB\n"
                f"データセグメント: {mem_usage.get('data', 0):.1f}MB\n"
                f"追跡オブジェクト数: {stats['tracked_objects']}\n"
                f"オブジェクトカウント: {stats['object_counts']}\n"
                f"GCオブジェクト数: {stats['gc_objects']}\n"
                f"ピークメモリ使用量: {stats['peak_memory_mb']:.1f}MB\n"
                f"起動からの経過時間: {stats['uptime_seconds']:.1f}秒"
            )
        except Exception as e:
            self.logger.error(f"トラッキング情報ログ出力エラー: {e}")

    def check_leaks(self):
        """メモリリークの検出"""
        try:
            gc.collect()
            snapshot = tracemalloc.take_snapshot()
            diff = snapshot.compare_to(self._initial_snapshot, 'traceback')
            
            if diff:
                self.logger.warning("\n=== 潜在的なメモリリーク ===")
                for stat in diff[:5]:
                    self.logger.warning(f"\n{stat.traceback.format()}")
                    self.logger.warning(f"サイズ: {stat.size / 1024:.1f}KB")
                    self.logger.warning(f"カウント: {stat.count}")
                    
        except Exception as e:
            self.logger.error(f"メモリリーク検出エラー: {e}")

    def cleanup(self):
        """トラッキングのクリーンアップ"""
        try:
            self.check_leaks()
            self._tracked_objects.clear()
            self._object_counts.clear()
            self._snapshots.clear()
            tracemalloc.stop()
            gc.collect()
        except Exception as e:
            self.logger.error(f"クリーンアップエラー: {e}")
