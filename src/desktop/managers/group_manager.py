import logging
from typing import List
from datetime import datetime
from src.desktop.models.group import Group
from src.desktop.database.database import Database
from src.desktop.utils.time_utils import TimeProvider

logger = logging.getLogger(__name__)

class GroupManager:
    """グループ管理クラス"""
    
    def __init__(self, database: Database):
        self.db = database
        self.current_time = TimeProvider.get_current_time()
        
    def create_group(self, name: str) -> Group:
        """グループを作成"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                current_time = datetime.now().isoformat()
                
                cursor.execute('''
                    INSERT INTO groups (name, created_at, updated_at)
                    VALUES (?, ?, ?)
                ''', (name, current_time, current_time))
                
                group_id = cursor.lastrowid
                conn.commit()
                
                return Group(
                    id=group_id,
                    name=name,
                    created_at=datetime.fromisoformat(current_time),
                    updated_at=datetime.fromisoformat(current_time)
                )
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to create group: {str(e)}")
            raise
            
    def get_group(self, group_id: int) -> Group:
        """グループを取得"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT * FROM groups WHERE id = ?', (group_id,))
                row = cursor.fetchone()
                
                if row:
                    return Group(
                        id=row[0],
                        name=row[1],
                        created_at=datetime.fromisoformat(row[2]),
                        updated_at=datetime.fromisoformat(row[3])
                    )
                return None
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get group: {str(e)}")
            raise
            
    def get_all_groups(self) -> List[Group]:
        """全グループを取得"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT * FROM groups ORDER BY name')
                rows = cursor.fetchall()
                
                return [
                    Group(
                        id=row[0],
                        name=row[1],
                        created_at=datetime.fromisoformat(row[2]),
                        updated_at=datetime.fromisoformat(row[3])
                    )
                    for row in rows
                ]
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get all groups: {str(e)}")
            raise
            
    def update_group(self, group_id: int, name: str) -> Group:
        """グループ情報を更新"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                current_time = datetime.now().isoformat()
                
                # 更新を実行
                cursor.execute('''
                    UPDATE groups
                    SET name = ?, updated_at = ?
                    WHERE id = ?
                ''', (name, current_time, group_id))
                
                if cursor.rowcount == 0:
                    raise ValueError(f"Group not found: {group_id}")
                    
                conn.commit()
                
                return Group(
                    id=group_id,
                    name=name,
                    created_at=None,  # 更新時は作成日時は不要
                    updated_at=datetime.fromisoformat(current_time)
                )
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to update group: {str(e)}")
            raise
            
    def delete_group(self, group_id: int) -> bool:
        """グループを削除"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                # 関連するユーザーのgroup_idをNullに設定
                cursor.execute('UPDATE users SET group_id = NULL WHERE group_id = ?', (group_id,))
                
                # グループを削除
                cursor.execute('DELETE FROM groups WHERE id = ?', (group_id,))
                conn.commit()
                
                return cursor.rowcount > 0
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to delete group: {str(e)}")
            raise