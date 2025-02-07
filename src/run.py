import sys
from PyQt6.QtWidgets import QApplication
import logging
from src.logging_config import setup_logging
from src.views.main_window import MainWindow

logger = logging.getLogger(__name__)

def main():
    setup_logging()
    logger.debug("Starting application")
    
    app = QApplication(sys.argv)
    window = MainWindow()
    logger.debug("Creating main window")
    
    window.show()
    logger.debug("Showing main window")
    
    logger.debug("Entering event loop")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
