import sys
import traceback
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from src.app import App
from src.debug_sync import setup_debug_logging, log_system_info

def main():
    """メイン実行関数"""
    logger = setup_debug_logging()
    log_system_info()
    
    try:
        logger.debug("Starting application")
        app = QApplication(sys.argv)
        
        # IMKClientの問題を回避するための設定
        app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar)
        
        # ウィンドウスタイルの設定
        app.setStyle('Fusion')
        
        window = App()
        window.show()
        
        logger.debug("Application main window shown")
        return app.exec()
        
    except Exception as e:
        logger.error(f"Critical error in main: {e}")
        logger.error(traceback.format_exc())
        return 1

if __name__ == '__main__':
    sys.exit(main())
