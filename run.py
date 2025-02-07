import sys
import logging
import signal
from datetime import datetime
from PyQt6.QtWidgets import QApplication
from src.app import App

def setup_logging():
    """ロギングの設定"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger()
    
    logger.debug("=== System Information ===")
    logger.debug(f"Python Version: {sys.version}")
    logger.debug(f"Platform: {sys.platform}")
    logger.debug(f"Current Time: {datetime.now().isoformat()}")
    logger.debug(f"Qt Version: {QApplication.instance().applicationVersion() if QApplication.instance() else 'Unknown'}")

def signal_handler(signum, frame):
    """シグナルハンドラ"""
    if QApplication.instance():
        QApplication.instance().quit()

def main():
    """メイン関数"""
    # シグナルハンドラの設定
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # ロギングの設定
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.debug("Starting application")
    
    try:
        # アプリケーションの作成と実行
        app = App(sys.argv)
        return app.start()
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
