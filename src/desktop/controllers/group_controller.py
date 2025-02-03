import logging
from typing import List
from src.desktop.models.group import Group
from src.desktop.managers.group_manager import GroupManager
from src.desktop.utils.time_utils import TimeProvider

logger = logging.getLogger(__name__)

class GroupController:
    """グループコントローラー"""
    
    def __init__(self, group_manager: GroupManager):
        self.group_manager = group_manager
        self.current_time = TimeProvider.get_current_time()
        
    def create_group(self, name: str) -> Group:
        """グループを作成"""
        try:
            group = self.group_manager.create_group(name)
            logger.debug(f"{self.current_time} - Created group: {name}")
            return group
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to create group: {str(e)}")
            raise
            
    def get_group(self, group_id: int) -> Group:
        """グループを取得"""
        try:
            group = self.group_manager.get_group(group_id)
            logger.debug(f"{self.current_time} - Retrieved group: {group.name}")
            return group
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get group: {str(e)}")
            raise
            
    def get_all_groups(self) -> List[Group]:
        """全グループを取得"""
        try:
            groups = self.group_manager.get_all_groups()
            logger.debug(f"{self.current_time} - Retrieved {len(groups)} groups")
            return groups
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get all groups: {str(e)}")
            raise
            
    def update_group(self, group_id: int, name: str) -> Group:
        """グループ情報を更新"""
        try:
            group = self.group_manager.update_group(group_id, name)
            logger.debug(f"{self.current_time} - Updated group: {group.name}")
            return group
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to update group: {str(e)}")
            raise
            
    def delete_group(self, group_id: int) -> bool:
        """グループを削除"""
        try:
            success = self.group_manager.delete_group(group_id)
            logger.debug(f"{self.current_time} - Deleted group: {group_id}")
            return success
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to delete group: {str(e)}")
            raise