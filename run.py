import sys
import logging
from PyQt6.QtWidgets import QApplication
from src.debug_sync import setup_logging
from src.app import App

def main():
    try:
        setup_logging()
        logger = logging.getLogger(__name__)
        
        app = QApplication(sys.argv)
        window = App()
        window.show()
        
        return app.exec()
        
    except Exception as e:
        logger.error(f"Critical error in main: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
