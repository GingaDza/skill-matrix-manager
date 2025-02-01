# src/desktop/gui/tabs/settings/section_base.py
"""
Base class for settings sections
Created: 2025-01-31 13:16:31
Author: GingaDza
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox
from ....models.data_manager import DataManager

class SettingsSectionBase(QWidget):
    def __init__(self, data_manager: DataManager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.group_box = None
        self.setup_ui()
        self.setup_signals()
    
    def setup_ui(self):
        """UI setup - override in subclasses"""
        self.layout = QVBoxLayout(self)
    
    def setup_signals(self):
        """Signal connections - override in subclasses"""
        pass
    
    def clear_inputs(self):
        """Clear input fields - override in subclasses"""
        pass
    
    def update_display(self):
        """Update display - override in subclasses"""
        pass