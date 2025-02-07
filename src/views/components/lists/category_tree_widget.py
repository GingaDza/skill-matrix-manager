from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
import logging

logger = logging.getLogger(__name__)

class CategoryTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        logger.debug("CategoryTreeWidget initialized")

    def setup_ui(self):
        self.setHeaderLabels(["カテゴリー/スキル"])
        self.setColumnCount(1)
        logger.debug("CategoryTreeWidget UI setup completed")

    def load_categories(self):
        try:
            self.clear()
            categories = self.parent.db.get_all_categories_with_skills()
            
            for category_id, category_name, skills in categories:
                category_item = QTreeWidgetItem([category_name])
                category_item.item_id = category_id
                self.addTopLevelItem(category_item)
                
                for skill_id, skill_name, description in skills:
                    skill_item = QTreeWidgetItem([skill_name])
                    skill_item.item_id = skill_id
                    skill_item.description = description
                    category_item.addChild(skill_item)
            
            self.expandAll()
            logger.debug(f"Loaded {len(categories)} categories")
        except Exception as e:
            logger.error(f"Error loading categories: {str(e)}")
            raise
