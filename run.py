import sys
import logging
from datetime import datetime
from PyQt6.QtWidgets import QApplication
from src.app import App
from logging_config import setup_logging

def main():
    """メイン関数"""
    # ログ設定
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # システム情報のログ出力
        logger.debug("=== System Information ===")
        logger.debug(f"Python Version: {sys.version}")
        logger.debug(f"Platform: {sys.platform}")
        logger.debug(f"Current Time: {datetime.now().isoformat()}")
        logger.debug(f"Qt Version: {QApplication.instance().applicationVersion() if QApplication.instance() else 'Unknown'}")
        
        logger.debug("Starting application")
        
        # アプリケーションの作成と実行
        app = App(sys.argv)
        return app.start()
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
