import sys
import logging
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
    
    # システム情報のログ
    logger.debug("=== System Information ===")
    logger.debug(f"Python Version: {sys.version}")
    logger.debug(f"Platform: {sys.platform}")
    logger.debug(f"Current Time: {datetime.now().isoformat()}")
    logger.debug(f"Qt Version: {QApplication.instance().applicationVersion() if QApplication.instance() else 'Unknown'}")

def main():
    """メイン関数"""
    # ロギングの設定
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.debug("Starting application")
    
    # アプリケーションの作成と実行
    app = App(sys.argv)
    logger.debug("Application main window shown")
    
    # イベントループの開始
    try:
        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
