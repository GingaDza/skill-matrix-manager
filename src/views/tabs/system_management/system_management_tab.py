from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
import logging

from src.views.tabs.system_management.group_manager import GroupManager
from src.views.tabs.system_management.category_manager import CategoryManager

logger = logging.getLogger(__name__)

class SystemManagementTab(QWidget):
    group_updated = pyqtSignal(list)
    category_added = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.db = self.parent.db if parent else None
        self.setup_ui()
        self.load_data()
        logger.debug("SystemManagementTab initialized")

    def setup_ui(self):
        layout = QHBoxLayout(self)
        
        # グループ管理セクション
        self.group_manager = GroupManager(self)
        layout.addWidget(self.group_manager)
        
        # カテゴリー管理セクション
        self.category_manager = CategoryManager(self)
        layout.addWidget(self.category_manager)
        
        logger.debug("SystemManagementTab UI setup completed")

    def load_data(self):
        try:
            self.group_manager.load_groups()
            self.category_manager.load_categories()
            logger.debug("SystemManagementTab data loaded")
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def emit_group_update(self):
        try:
            groups = [self.group_manager.group_list.item(i).text() 
                     for i in range(self.group_manager.group_list.count())]
            self.group_updated.emit(groups)
            logger.debug(f"Group update signal emitted with {len(groups)} groups")
        except Exception as e:
            logger.error(f"Error emitting group update: {str(e)}")
            raise
