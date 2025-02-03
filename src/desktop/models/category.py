# src/desktop/models/category.py
import logging
from typing import List, Optional
from ..services.db import DatabaseManager
from ..utils.time_utils import TimeProvider

logger = logging.getLogger(__name__)

class Category:
    """カテゴリーモデル"""
    
    def __init__(self, id: int, name: str, description: str = None, parent_id: int = None):
        self.id = id
        self.name = name
        self.description = description
        self.parent_id = parent_id

class CategoryManager:
    """カテゴリー管理クラス"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.current_time = TimeProvider.get_current_time()
        self.current_user = TimeProvider.get_current_user()
        
        self.db = db_manager
        logger.debug(f"{self.current_time} - CategoryManager initialized")

    def create_category(self, name: str, description: str = None, parent_id: Optional[int] = None) -> int:
        """
        新しいカテゴリーを作成
        
        Args:
            name: カテゴリー名
            description: 説明
            parent_id: 親カテゴリーID
            
        Returns:
            int: 作成されたカテゴリーのID
        """
        try:
            cursor = self.db.connection.cursor()
            cursor.execute(
                """
                INSERT INTO categories (name, description, parent_id)
                VALUES (?, ?, ?)
                """,
                (name, description, parent_id)
            )
            self.db.connection.commit()
            category_id = cursor.lastrowid
            logger.debug(f"{self.current_time} - Created category: {name} (ID: {category_id})")
            return category_id
        except Exception as e:
            self.db.connection.rollback()
            logger.error(f"{self.current_time} - Failed to create category: {str(e)}")
            raise

    def get_category(self, category_id: int) -> Optional[Category]:
        """
        カテゴリーを取得
        
        Args:
            category_id: カテゴリーID
            
        Returns:
            Category: カテゴリーオブジェクト
        """
        try:
            cursor = self.db.connection.cursor()
            cursor.execute(
                "SELECT id, name, description, parent_id FROM categories WHERE id = ?",
                (category_id,)
            )
            row = cursor.fetchone()
            if row:
                return Category(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    parent_id=row[3]
                )
            return None
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get category: {str(e)}")
            raise

    def get_all_categories(self) -> List[Category]:
        """
        全てのカテゴリーを取得
        
        Returns:
            List[Category]: カテゴリーオブジェクトのリスト
        """
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT id, name, description, parent_id FROM categories")
            return [
                Category(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    parent_id=row[3]
                )
                for row in cursor.fetchall()
            ]
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get all categories: {str(e)}")
            raise

    def update_category(self, category_id: int, name: str, description: str = None) -> bool:
        """
        カテゴリーを更新
        
        Args:
            category_id: カテゴリーID
            name: 新しいカテゴリー名
            description: 新しい説明
            
        Returns:
            bool: 更新が成功したかどうか
        """
        try:
            cursor = self.db.connection.cursor()
            cursor.execute(
                """
                UPDATE categories
                SET name = ?, description = ?
                WHERE id = ?
                """,
                (name, description, category_id)
            )
            self.db.connection.commit()
            success = cursor.rowcount > 0
            if success:
                logger.debug(f"{self.current_time} - Updated category: {name} (ID: {category_id})")
            return success
        except Exception as e:
            self.db.connection.rollback()
            logger.error(f"{self.current_time} - Failed to update category: {str(e)}")
            raise

    def delete_category(self, category_id: int) -> bool:
        """
        カテゴリーを削除
        
        Args:
            category_id: カテゴリーID
            
        Returns:
            bool: 削除が成功したかどうか
        """
        try:
            cursor = self.db.connection.cursor()
            # 子カテゴリーを再帰的に削除
            cursor.execute("SELECT id FROM categories WHERE parent_id = ?", (category_id,))
            for (child_id,) in cursor.fetchall():
                self.delete_category(child_id)
            
            # このカテゴリーを削除
            cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
            self.db.connection.commit()
            success = cursor.rowcount > 0
            if success:
                logger.debug(f"{self.current_time} - Deleted category ID: {category_id}")
            return success
        except Exception as e:
            self.db.connection.rollback()
            logger.error(f"{self.current_time} - Failed to delete category: {str(e)}")
            raise