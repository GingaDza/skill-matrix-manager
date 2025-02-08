"""グループ操作のミックスイン"""
import sqlite3
from typing import Optional

class GroupManagerMixin:
    """グループ操作を提供するミックスイン"""

    def get_groups(self) -> list[str]:
        """
        グループの一覧を取得する
        
        Returns:
            list[str]: グループ名のリスト
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT name FROM groups ORDER BY name"
                )
                return [row[0] for row in cursor.fetchall()]
                
        except sqlite3.Error as e:
            self.logger.exception("グループ取得エラー", exc_info=e)
            return []

    def add_group(self, name: str) -> bool:
        """
        グループを追加する
        
        Args:
            name (str): グループ名
            
        Returns:
            bool: 追加に成功した場合はTrue、失敗した場合はFalse
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO groups (name, created_at, updated_at)
                    VALUES (?, ?, ?)
                    """,
                    (name, self.current_time, self.current_time)
                )
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            self.logger.exception("グループ追加エラー", exc_info=e)
            return False

    def rename_group(self, old_name: str, new_name: str) -> bool:
        """
        グループ名を変更する
        
        Args:
            old_name (str): 現在のグループ名
            new_name (str): 新しいグループ名
            
        Returns:
            bool: 変更に成功した場合はTrue、失敗した場合はFalse
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE groups
                    SET name = ?, updated_at = ?
                    WHERE name = ?
                    """,
                    (new_name, self.current_time, old_name)
                )
                conn.commit()
                return cursor.rowcount > 0
                
        except sqlite3.Error as e:
            self.logger.exception("グループ名変更エラー", exc_info=e)
            return False

    def delete_group(self, name: str) -> bool:
        """
        グループを削除する
        
        Args:
            name (str): グループ名
            
        Returns:
            bool: 削除に成功した場合はTrue、失敗した場合はFalse
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # グループのIDを取得
                cursor.execute(
                    "SELECT group_id FROM groups WHERE name = ?",
                    (name,)
                )
                group_id = cursor.fetchone()
                
                if group_id:
                    # 関連するカテゴリーのIDを取得
                    cursor.execute(
                        "SELECT category_id FROM categories WHERE group_id = ?",
                        (group_id[0],)
                    )
                    category_ids = cursor.fetchall()
                    
                    # 関連するスキルを削除
                    for category_id in category_ids:
                        cursor.execute(
                            "DELETE FROM skills WHERE parent_id = ?",
                            (category_id[0],)
                        )
                    
                    # カテゴリーを削除
                    cursor.execute(
                        "DELETE FROM categories WHERE group_id = ?",
                        (group_id[0],)
                    )
                    
                    # グループを削除
                    cursor.execute(
                        "DELETE FROM groups WHERE group_id = ?",
                        (group_id[0],)
                    )
                    
                    conn.commit()
                    return True
                    
                return False
                
        except sqlite3.Error as e:
            self.logger.exception("グループ削除エラー", exc_info=e)
            return False

    def get_group_id_by_name(self, name: str) -> Optional[int]:
        """
        グループ名からIDを取得する
        
        Args:
            name (str): グループ名
            
        Returns:
            Optional[int]: グループID。グループが見つからない場合はNone
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT group_id FROM groups WHERE name = ?",
                    (name,)
                )
                result = cursor.fetchone()
                return result[0] if result else None
                
        except sqlite3.Error as e:
            self.logger.exception("グループID取得エラー", exc_info=e)
            return None
