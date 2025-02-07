import logging
import sys
import platform
from datetime import datetime

def setup_logging():
    """ロギングの設定"""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # コンソールハンドラの設定
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    # フォーマッタの設定
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    # ロガーにハンドラを追加
    logger.addHandler(console_handler)

    # システム情報をログに記録
    logger.debug("=== System Information ===")
    logger.debug(f"Python Version: {sys.version}")
    logger.debug(f"Platform: {platform.system().lower()}")
    logger.debug(f"Current Time: {datetime.now().isoformat()}")
    logger.debug(f"Qt Version: 6.8.1")
    logger.debug("Starting application")

# アプリケーション起動時の初期化
def initialize_app():
    setup_logging()
