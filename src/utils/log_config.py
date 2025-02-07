"""ロギング設定"""
import logging
import sys
from typing import Optional
from logging.handlers import RotatingFileHandler
import os

class MemoryAwareLogger:
    """メモリ使用量を考慮したロガー"""
    
    def __init__(self):
        self.logger = logging.getLogger('MemoryManager')
        self._configure_logger()
        self._debug_mode = False

    def _configure_logger(self):
        """ロガーの設定"""
        self.logger.setLevel(logging.INFO)
        
        # フォーマッターの設定
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        )
        
        # コンソールハンドラー
        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(formatter)
        self.logger.addHandler(console)
        
        # ファイルハンドラー
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, 'memory.log'),
            maxBytes=1024 * 1024,  # 1MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def set_debug_mode(self, enabled: bool):
        """デバッグモードの設定"""
        self._debug_mode = enabled
        self.logger.setLevel(
            logging.DEBUG if enabled else logging.INFO
        )

    def log_memory_stats(self, stats: dict):
        """メモリ統計情報のログ出力"""
        if self._debug_mode:
            self.logger.debug("=== Memory Statistics ===")
            for key, value in stats.items():
                self.logger.debug(f"{key}: {value}")
        else:
            # 重要な情報のみ出力
            if stats.get('warning'):
                self.logger.warning(stats['warning'])
            if stats.get('error'):
                self.logger.error(stats['error'])

    def log_object_stats(self, stats: dict):
        """オブジェクト統計情報のログ出力"""
        if self._debug_mode:
            self.logger.debug("=== Object Statistics ===")
            for key, value in stats.items():
                self.logger.debug(f"{key}: {value}")

    def log_leak_detection(self, leaks: list):
        """メモリリーク検出情報のログ出力"""
        if leaks:
            self.logger.warning("Memory Leaks Detected:")
            for leak in leaks:
                self.logger.warning(f"  {leak}")

# グローバルロガーインスタンス
memory_logger = MemoryAwareLogger()
