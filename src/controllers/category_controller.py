from ..models.category import Category
from ..database.database_manager import DatabaseManager

class CategoryController:
    """カテゴリーのコントローラー"""

    def __init__(self, db=None):
        self.db = db if db else DatabaseManager()

    def create_category(self, name, description="", parent_id=None):
        """カテゴリーを作成"""
        try:
            category_id = self.db.add_category(name, description, parent_id)
            return category_id
        except Exception as e:
            print(f"カテゴリーの作成に失敗: {e}")
            return None

    def get_category(self, category_id):
        """カテゴリーを取得"""
        try:
            data = self.db.get_category(category_id)
            if data:
                category = Category(
                    id=data[0],
                    name=data[1],
                    description=data[2],
                    parent_id=data[3]
                )
                return category
            return None
        except Exception as e:
            print(f"カテゴリーの取得に失敗: {e}")
            return None

    def get_all_categories(self):
        """すべてのカテゴリーを取得"""
        try:
            categories = []
            data = self.db.get_all_categories()
            for row in data:
                category = Category(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    parent_id=row[3]
                )
                categories.append(category)
            return categories
        except Exception as e:
            print(f"カテゴリー一覧の取得に失敗: {e}")
            return []

    def update_category(self, category_id, name, description="", parent_id=None):
        """カテゴリーを更新"""
        try:
            success = self.db.update_category(
                category_id,
                name,
                description,
                parent_id
            )
            return success
        except Exception as e:
            print(f"カテゴリーの更新に失敗: {e}")
            return False

    def delete_category(self, category_id):
        """カテゴリーを削除"""
        try:
            success = self.db.delete_category(category_id)
            return success
        except Exception as e:
            print(f"カテゴリーの削除に失敗: {e}")
            return False

    def get_category_hierarchy(self):
        """カテゴリーの階層構造を取得"""
        try:
            return self.db.get_category_hierarchy()
        except Exception as e:
            print(f"カテゴリー階層の取得に失敗: {e}")
            return []
