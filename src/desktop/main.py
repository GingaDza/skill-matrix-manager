import sys
from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow
import logging
from datetime import datetime

# デバッグ用にログ設定
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

CURRENT_TIME = datetime(2025, 2, 3, 10, 39, 38)
CURRENT_USER = "GingaDza"

def main():
    logger.debug(f"{CURRENT_TIME} - {CURRENT_USER} Application starting")
    
    try:
        app = QApplication(sys.argv)
        logger.debug(f"{CURRENT_TIME} - {CURRENT_USER} QApplication created")
        
        window = MainWindow(controllers=None)
        logger.debug(f"{CURRENT_TIME} - {CURRENT_USER} MainWindow created")
        
        window.show()
        logger.debug(f"{CURRENT_TIME} - {CURRENT_USER} MainWindow shown")
        
        return_code = app.exec()
        logger.debug(f"{CURRENT_TIME} - {CURRENT_USER} Application finished with return code: {return_code}")
        sys.exit(return_code)
        
    except Exception as e:
        logger.error(f"{CURRENT_TIME} - {CURRENT_USER} Application error: {str(e)}")
        logger.exception("Detailed traceback:")
        sys.exit(1)

if __name__ == "__main__":
    main()