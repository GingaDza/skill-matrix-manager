import sys
import logging
from datetime import datetime

def setup_debug_logging():
    """デバッグ用のロギング設定"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('debug.log')
        ]
    )
    return logging.getLogger(__name__)

def log_system_info():
    """システム情報をログに記録"""
    logger = logging.getLogger(__name__)
    logger.debug("=== System Information ===")
    logger.debug(f"Python Version: {sys.version}")
    logger.debug(f"Platform: {sys.platform}")
    logger.debug(f"Current Time: {datetime.now().isoformat()}")
    
    try:
        from PyQt6.QtCore import QT_VERSION_STR
        logger.debug(f"Qt Version: {QT_VERSION_STR}")
    except ImportError as e:
        logger.error(f"Qt import error: {e}")

