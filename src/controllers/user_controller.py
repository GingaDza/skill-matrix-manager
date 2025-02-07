import logging
from typing import List
from src.desktop.models.user import User
from src.desktop.managers.user_manager import UserManager
from src.desktop.utils.time_utils import TimeProvider

logger = logging.getLogger(__name__)

class UserController:
    """ユーザーコントローラー"""
    
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager
        self.current_time = TimeProvider.get_current_time()
        
    def create_user(self, employee_id: str, name: str, group_id: int = None) -> User:
        """ユーザーを作成"""
        try:
            user = self.user_manager.create_user(employee_id, name, group_id)
            logger.debug(f"{self.current_time} - Created user: {name}")
            return user
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to create user: {str(e)}")
            raise
            
    def get_user(self, user_id: int) -> User:
        """ユーザーを取得"""
        try:
            user = self.user_manager.get_user(user_id)
            logger.debug(f"{self.current_time} - Retrieved user: {user.name}")
            return user
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get user: {str(e)}")
            raise
            
    def get_all_users(self) -> List[User]:
        """全ユーザーを取得"""
        try:
            users = self.user_manager.get_all_users()
            logger.debug(f"{self.current_time} - Retrieved {len(users)} users")
            return users
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get all users: {str(e)}")
            raise
            
    def get_users_by_group(self, group_id: int) -> List[User]:
        """グループに属するユーザーを取得"""
        try:
            users = self.user_manager.get_users_by_group(group_id)
            logger.debug(f"{self.current_time} - Retrieved {len(users)} users for group {group_id}")
            return users
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get users by group: {str(e)}")
            raise
            
    def update_user(self, user_id: int, employee_id: str = None, name: str = None, group_id: int = None) -> User:
        """ユーザー情報を更新"""
        try:
            user = self.user_manager.update_user(user_id, employee_id, name, group_id)
            logger.debug(f"{self.current_time} - Updated user: {user.name}")
            return user
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to update user: {str(e)}")
            raise
            
    def delete_user(self, user_id: int) -> bool:
        """ユーザーを削除"""
        try:
            success = self.user_manager.delete_user(user_id)
            logger.debug(f"{self.current_time} - Deleted user: {user_id}")
            return success
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to delete user: {str(e)}")
            raise