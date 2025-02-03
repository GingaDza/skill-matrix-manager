from PyQt6.QtWidgets import QListWidget, QListWidgetItem
import logging
from src.desktop.utils.time_utils import TimeProvider

logger = logging.getLogger(__name__)

class UserListWidget(QListWidget):
    def __init__(self, user_controller, parent=None):
        super().__init__(parent)
        self.user_controller = user_controller
        self.current_time = TimeProvider.get_current_time()
        
    def add_user(self, user):
        """ユーザーをリストに追加"""
        try:
            item = QListWidgetItem(f"{user.employee_id} - {user.name}")
            item.user = user
            self.addItem(item)
            logger.debug(f"{self.current_time} - Added user to list: {user.name}")
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to add user to list: {str(e)}")
            raise
            
    def get_selected_user(self):
        """選択されているユーザーを取得"""
        try:
            current_item = self.currentItem()
            if current_item:
                return current_item.user
            return None
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get selected user: {str(e)}")
            raise