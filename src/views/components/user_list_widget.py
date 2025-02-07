from PyQt6.QtWidgets import QListWidget, QListWidgetItem
import logging

logger = logging.getLogger(__name__)

class UserListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        logger.debug("UserListWidget initialized")

    def load_users(self, group_id):
        try:
            self.clear()
            users = self.parent.db.get_users_by_group(group_id)
            for user_id, name, email in users:
                item = QListWidgetItem(name)
                item.setToolTip(email if email else "")
                item.user_id = user_id
                self.addItem(item)
            logger.debug(f"Loaded {len(users)} users for group {group_id}")
        except Exception as e:
            logger.error(f"Error loading users: {str(e)}")
            raise
