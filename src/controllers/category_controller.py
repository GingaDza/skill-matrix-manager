# src/desktop/controllers/category_controller.py
from typing import List, Optional
from ..models.category import Category, CategoryManager
import logging
from ..utils.time_utils import TimeProvider

logger = logging.getLogger(__name__)

class CategoryController:
    """カテゴリーコントローラー"""
    
    def __init__(self, category_manager: CategoryManager):
        self.current_time = TimeProvider.get_current_time()
        self.current_user = TimeProvider.get_current_user()
        
        self.category_manager = category_manager
        logger.debug(f"{self.current_time} - CategoryController initialized")

    def create_category(self, name: str, description: str = None, parent_id: Optional[int] = None) -> int:
        """カテゴリーを作成"""
        try:
            category_id = self.category_manager.create_category(name, description, parent_id)
            logger.debug(f"{self.current_time} - Created category: {name} (ID: {category_id})")
            return category_id
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to create category: {str(e)}")
            raise

    def get_category(self, category_id: int) -> Category:
        """カテゴリーを取得"""
        try:
            category = self.category_manager.get_category(category_id)
            if category is None:
                raise ValueError(f"Category with ID {category_id} not found")
            return category
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get category {category_id}: {str(e)}")
            raise

    def get_all_categories(self) -> List[Category]:
        """全てのカテゴリーを取得"""
        try:
            return self.category_manager.get_all_categories()
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get all categories: {str(e)}")
            raise

    def update_category(self, category_id: int, name: str, description: str = None) -> bool:
        """カテゴリーを更新"""
        try:
            success = self.category_manager.update_category(category_id, name, description)
            if success:
                logger.debug(f"{self.current_time} - Updated category: {name} (ID: {category_id})")
            return success
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to update category: {str(e)}")
            raise

    def delete_category(self, category_id: int) -> bool:
        """カテゴリーを削除"""
        try:
            success = self.category_manager.delete_category(category_id)
            if success:
                logger.debug(f"{self.current_time} - Deleted category ID: {category_id}")
            return success
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to delete category: {str(e)}")
            raise