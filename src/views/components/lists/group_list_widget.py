from PyQt6.QtWidgets import QListWidget, QListWidgetItem
import logging

logger = logging.getLogger(__name__)

class GroupListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        logger.debug("GroupListWidget initialized")

    def load_groups(self):
        try:
            self.clear()
            groups = self.parent.db.get_all_groups()
            
            for group_id, name, user_count in groups:
                item = QListWidgetItem(f"{name} ({user_count}人)")
                item.item_id = group_id
                self.addItem(item)
            
            logger.debug(f"Loaded {len(groups)} groups")
        except Exception as e:
            logger.error(f"Error loading groups: {str(e)}")
            raise
