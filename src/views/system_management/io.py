"""データ入出力ウィジェット"""
import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox,
    QPushButton, QFileDialog
)
from ...database.database_manager import DatabaseManager

class IOWidget(QWidget):
    """データ入出力タブのウィジェット"""
    
    def __init__(self, db_manager: DatabaseManager, parent: QWidget = None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self._db_manager = db_manager
        self._init_ui()

    # [以下のメソッドは前回と同じ]
