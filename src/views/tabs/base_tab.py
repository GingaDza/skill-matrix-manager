from PyQt6.QtWidgets import QWidget, QMessageBox
import logging

logger = logging.getLogger(__name__)

class BaseTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.db = parent.db if parent else None
        logger.debug(f"{self.__class__.__name__} initialized")

    def show_error(self, message):
        QMessageBox.critical(self, "エラー", message)
        logger.error(f"Error dialog shown: {message}")

    def show_warning(self, message):
        QMessageBox.warning(self, "警告", message)
        logger.warning(f"Warning dialog shown: {message}")

    def show_info(self, message):
        QMessageBox.information(self, "情報", message)
        logger.info(f"Info dialog shown: {message}")

    def confirm_delete(self, message):
        reply = QMessageBox.question(
            self, '確認', 
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        result = reply == QMessageBox.StandardButton.Yes
        logger.debug(f"Delete confirmation dialog result: {result}")
        return result
