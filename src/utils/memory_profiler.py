"""メモリプロファイリングユーティリティ"""
import gc
import tracemalloc
import psutil
import os
from typing import Dict, List, Any
from collections import Counter
from PyQt6.QtCore import QObject
from .log_config import memory_logger

class MemoryProfiler:
    """メモリ使用状況の分析クラス"""
    
    def __init__(self):
        self._snapshot = None
        tracemalloc.start()
        self._warning_threshold_mb = 512  # 警告閾値: 512MB
        self._error_threshold_mb = 1024   # エラー閾値: 1GB

    def take_snapshot(self) -> None:
        """メモリスナップショットの取得"""
        self._snapshot = tracemalloc.take_snapshot()

    def analyze_memory_usage(self) -> Dict[str, Any]:
        """メモリ使用状況の分析"""
        process = psutil.Process()
        mem_info = process.memory_full_info()
        
        rss_mb = mem_info.rss / (1024 * 1024)
        vms_mb = mem_info.vms / (1024 * 1024)
        
        stats = {
            'rss_mb': rss_mb,
            'vms_mb': vms_mb,
            'warning': None,
            'error': None
        }
        
        if vms_mb > self._error_threshold_mb:
            stats['error'] = f"危険な高メモリ使用量: {vms_mb:.1f}MB"
        elif vms_mb > self._warning_threshold_mb:
            stats['warning'] = f"高メモリ使用量: {vms_mb:.1f}MB"
        
        memory_logger.log_memory_stats(stats)
        return stats

    def analyze_object_stats(self) -> Dict[str, int]:
        """オブジェクト統計の分析"""
        qt_objects = [obj for obj in gc.get_objects() 
                     if isinstance(obj, QObject)]
        stats = Counter(type(obj).__name__ for obj in qt_objects)
        
        if memory_logger._debug_mode:
            memory_logger.log_object_stats(dict(stats))
        
        return dict(stats)

    def find_memory_leaks(self) -> List[str]:
        """メモリリークの検出"""
        leaks = []
        for obj in gc.get_objects():
            if isinstance(obj, QObject):
                try:
                    refs = gc.get_referrers(obj)
                    if len(refs) > 2:  # 通常の参照以外の余分な参照がある
                        leaks.append(
                            f"{type(obj).__name__}: {len(refs)}件の参照"
                        )
                except Exception:
                    pass
        
        memory_logger.log_leak_detection(leaks)
        return leaks

    def cleanup(self) -> None:
        """プロファイラーのクリーンアップ"""
        tracemalloc.stop()
        gc.collect()
