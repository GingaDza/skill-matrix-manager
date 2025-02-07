# src/desktop/views/components/categories/category_manager_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout
import logging
from ....controllers.category_controller import CategoryController
from .category_tree_widget import CategoryTreeWidget
from ....utils.time_utils import TimeProvider

logger = logging.getLogger(__name__)

class CategoryManagerWidget(QWidget):
    """カテゴリー管理ウィジェット"""
    
    def __init__(self, category_controller: CategoryController):
        super().__init__()
        self.current_time = TimeProvider.get_current_time()
        self.current_user = TimeProvider.get_current_user()
        
        self.category_controller = category_controller
        self.setup_ui()
        
        logger.debug(f"{self.current_time} - CategoryManagerWidget initialized")

    def setup_ui(self):
        """UIのセットアップ"""
        try:
            layout = QVBoxLayout(self)
            
            # カテゴリーツリー
            self.category_tree = CategoryTreeWidget(self.category_controller)
            layout.addWidget(self.category_tree)
            
            logger.debug(f"{self.current_time} - CategoryManagerWidget UI setup completed")
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to setup CategoryManagerWidget UI: {str(e)}")
            raise

    def refresh_categories(self):
        """カテゴリーツリーを更新"""
        try:
            self.category_tree.refresh_categories()
            logger.debug(f"{self.current_time} - CategoryManagerWidget refreshed categories")
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to refresh CategoryManagerWidget: {str(e)}")