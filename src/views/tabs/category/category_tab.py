# src/views/tabs/category/category_tab.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
import logging

logger = logging.getLogger(__name__)

class CategoryTab(QWidget):
    def __init__(self, category_name, parent=None):
        super().__init__(parent)
        self.category_name = category_name
        self.parent = parent
        self.setup_ui()
        logger.debug(f"CategoryTab initialized for category: {category_name}")

    def setup_ui(self):
        layout = QVBoxLayout(self)
        label = QLabel(f"カテゴリー: {self.category_name}")
        layout.addWidget(label)
        logger.debug(f"CategoryTab UI setup completed for: {self.category_name}")