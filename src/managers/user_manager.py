import logging
from typing import List
from datetime import datetime
from src.desktop.models.user import User
from src.desktop.database.database import Database
from src.desktop.utils.time_utils import TimeProvider

logger = logging.getLogger(__name__)

class UserManager:
    """ユーザー管理クラス"""
    
    def __init__(self, database: Database):
        self.db = database
        self.current_time = TimeProvider.get_current_time()
        
    def create_user(self, employee_id: str, name: str, group_id: int = None) -> User:
        """ユーザーを作成"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                current_time = datetime.now().isoformat()
                
                cursor.execute('''
                    INSERT INTO users (employee_id, name, group_id, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (employee_id, name, group_id, current_time, current_time))
                
                user_id = cursor.lastrowid
                conn.commit()
                
                return User(
                    id=user_id,
                    employee_id=employee_id,
                    name=name,
                    group_id=group_id,
                    created_at=datetime.fromisoformat(current_time),
                    updated_at=datetime.fromisoformat(current_time)
                )
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to create user: {str(e)}")
            raise
            
    def get_user(self, user_id: int) -> User:
        """ユーザーを取得"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
                row = cursor.fetchone()
                
                if row:
                    return User(
                        id=row[0],
                        employee_id=row[1],
                        name=row[2],
                        group_id=row[3],
                        created_at=datetime.fromisoformat(row[4]),
                        updated_at=datetime.fromisoformat(row[5])
                    )
                return None
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get user: {str(e)}")
            raise
            
    def get_all_users(self) -> List[User]:
        """全ユーザーを取得"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT * FROM users ORDER BY employee_id')
                rows = cursor.fetchall()
                
                return [
                    User(
                        id=row[0],
                        employee_id=row[1],
                        name=row[2],
                        group_id=row[3],
                        created_at=datetime.fromisoformat(row[4]),
                        updated_at=datetime.fromisoformat(row[5])
                    )
                    for row in rows
                ]
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get all users: {str(e)}")
            raise
            
    def get_users_by_group(self, group_id: int) -> List[User]:
        """グループに属するユーザーを取得"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT * FROM users WHERE group_id = ? ORDER BY employee_id', (group_id,))
                rows = cursor.fetchall()
                
                return [
                    User(
                        id=row[0],
                        employee_id=row[1],
                        name=row[2],
                        group_id=row[3],
                        created_at=datetime.fromisoformat(row[4]),
                        updated_at=datetime.fromisoformat(row[5])
                    )
                    for row in rows
                ]
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get users by group: {str(e)}")
            raise
            
    def update_user(self, user_id: int, employee_id: str = None, name: str = None, group_id: int = None) -> User:
        """ユーザー情報を更新"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                current_time = datetime.now().isoformat()
                
                # 現在のユーザー情報を取得
                cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
                row = cursor.fetchone()
                
                if not row:
                    raise ValueError(f"User not found: {user_id}")
                    
                # 更新するフィールドを設定
                update_employee_id = employee_id if employee_id is not None else row[1]
                update_name = name if name is not None else row[2]
                update_group_id = group_id if group_id is not None else row[3]
                
                # 更新を実行
                cursor.execute('''
                    UPDATE users
                    SET employee_id = ?, name = ?, group_id = ?, updated_at = ?
                    WHERE id = ?
                ''', (update_employee_id, update_name, update_group_id, current_time, user_id))
                
                conn.commit()
                
                return User(
                    id=user_id,
                    employee_id=update_employee_id,
                    name=update_name,
                    group_id=update_group_id,
                    created_at=datetime.fromisoformat(row[4]),
                    updated_at=datetime.fromisoformat(current_time)
                )
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to update user: {str(e)}")
            raise
            
    def delete_user(self, user_id: int) -> bool:
        """ユーザーを削除"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
                conn.commit()
                
                return cursor.rowcount > 0
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to delete user: {str(e)}")
            raise