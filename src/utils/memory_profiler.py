"""メモリプロファイリングユーティリティ"""
import gc
import tracemalloc
import psutil
import os
import logging
from typing import Dict, List, Any
from collections import Counter
from PyQt6.QtCore import QObject

class MemoryProfiler:
    """メモリ使用状況の分析クラス"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._snapshot = None
        tracemalloc.start()

    def take_snapshot(self) -> None:
        """メモリスナップショットの取得"""
        self._snapshot = tracemalloc.take_snapshot()

    def compare_to_baseline(self) -> None:
        """ベースラインとの比較"""
        if self._snapshot is None:
            self.logger.warning("ベースラインスナップショットがありません")
            return
            
        current = tracemalloc.take_snapshot()
        diff = current.compare_to(self._snapshot, 'lineno')
        
        for stat in diff[:10]:
            self.logger.debug(f"{stat.size_diff / 1024:.1f}KB {stat.count_diff:+d}: {stat.traceback}")

    def analyze_qt_objects(self) -> Dict[str, int]:
        """Qtオブジェクトの分析"""
        qt_objects = [obj for obj in gc.get_objects() 
                     if isinstance(obj, QObject)]
        return Counter(type(obj).__name__ for obj in qt_objects)

    def analyze_memory_usage(self) -> Dict[str, Any]:
        """メモリ使用状況の詳細分析"""
        process = psutil.Process(os.getpid())
        mem_info = process.memory_full_info()
        
        return {
            'rss': mem_info.rss / (1024 * 1024),
            'vms': mem_info.vms / (1024 * 1024),
            'uss': mem_info.uss / (1024 * 1024),
            'qt_objects': self.analyze_qt_objects(),
            'gc_count': gc.get_count(),
            'gc_objects': len(gc.get_objects())
        }

    def find_memory_leaks(self) -> List[str]:
        """メモリリークの検出"""
        leaks = []
        for obj in gc.get_objects():
            if isinstance(obj, QObject):
                try:
                    refs = gc.get_referrers(obj)
                    if len(refs) > 2:
                        leaks.append(
                            f"{type(obj).__name__}: {len(refs)}件の参照"
                        )
                except Exception:
                    pass
        return leaks

    def cleanup(self) -> None:
        """プロファイラーのクリーンアップ"""
        tracemalloc.stop()
        gc.collect()
