from PyQt6.QtWidgets import QGroupBox
from .category_ui_manager import CategoryUIManager
from .category_data_manager import CategoryDataManager
from .category_event_handler import CategoryEventHandler
from .debug_logger import DebugLogger

class CategorySection(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("カテゴリー管理", parent)
        
        # 各マネージャーの初期化
        self.debug_logger = DebugLogger()
        self.data_manager = CategoryDataManager(self.debug_logger)
        self.ui_manager = CategoryUIManager(self, self.debug_logger)
        self.event_handler = CategoryEventHandler(
            self, self.data_manager, self.ui_manager, self.debug_logger)
        
        self.setup()
        
    def setup(self):
        self.debug_logger.log_debug("CategorySection initialization started")
        self.ui_manager.setup_ui()
        self.event_handler.setup_connections()
        self.debug_logger.log_debug("CategorySection initialization completed")

    def set_selected_group(self, group_name):
        self.debug_logger.log_method_call("set_selected_group", group_name=group_name)
        return self.data_manager.set_selected_group(group_name)