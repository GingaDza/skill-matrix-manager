# src/views/tabs/system_management/base_classes.py

from PyQt6.QtWidgets import QListWidgetItem, QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox
import logging

logger = logging.getLogger(__name__)

class ListItemWithId(QListWidgetItem):
    def __init__(self, text, item_id):
        super().__init__(text)
        self.item_id = item_id

class AddEditDialog(QDialog):
    def __init__(self, parent=None, title="", initial_text=""):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setup_ui(initial_text)
        logger.debug(f"AddEditDialog initialized with title: {title}")

    def setup_ui(self, initial_text):
        layout = QVBoxLayout(self)
        
        self.name_input = QLineEdit(initial_text)
        layout.addWidget(self.name_input)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        logger.debug("AddEditDialog UI setup completed")

    def get_name(self):
        return self.name_input.text().strip()