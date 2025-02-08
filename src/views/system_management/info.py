"""システム情報ウィジェット"""
import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox,
    QLabel, QListWidget, QPushButton,
    QFileDialog
)
from ...database.database_manager import DatabaseManager

class InfoWidget(QWidget):
    """システム情報タブのウィジェット"""
    
    def __init__(self, db_manager: DatabaseManager, parent: QWidget = None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self._db_manager = db_manager
        self._init_ui()

    # [以下のメソッドは前回と同じ]
