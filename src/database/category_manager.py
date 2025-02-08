"""カテゴリー操作のミックスイン"""
import sqlite3
from typing import Optional

class CategoryManagerMixin:
    """カテゴリー操作を提供するミックスイン"""

    def get_parent_categories_by_group(self, group_id: int) -> list[str]:
        """
        グループに属する親カテゴリーの一覧を取得する
        
        Args:
            group_id (int): グループID
            
        Returns:
            list[str]: カテゴリー名のリスト
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    """
                    SELECT name
                    FROM categories
                    WHERE group_id = ?
                    ORDER BY name
                    """,
                    (group_id,)
                )
                
                return [row[0] for row in cursor.fetchall()]
                
        except sqlite3.Error as e:
            self.logger.exception("カテゴリー取得エラー", exc_info=e)
            return []

    def add_parent_category(self, name: str, group_id: int) -> bool:
        """
        親カテゴリーを追加する
        
        Args:
            name (str): カテゴリー名
            group_id (int): グループID
            
        Returns:
            bool: 追加に成功した場合はTrue、失敗した場合はFalse
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    """
                    INSERT INTO categories (name, group_id, created_at, updated_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (name, group_id, self.current_time, self.current_time)
                )
                conn.commit()
                return True
                    
        except sqlite3.Error as e:
            self.logger.exception("カテゴリー追加エラー", exc_info=e)
            return False

    def rename_parent_category(self, old_name: str, new_name: str, group_id: int) -> bool:
        """
        親カテゴリー名を変更する
        
        Args:
            old_name (str): 現在のカテゴリー名
            new_name (str): 新しいカテゴリー名
            group_id (int): グループID
            
        Returns:
            bool: 変更に成功した場合はTrue、失敗した場合はFalse
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    """
                    UPDATE categories
                    SET name = ?, updated_at = ?
                    WHERE name = ? AND group_id = ?
                    """,
                    (new_name, self.current_time, old_name, group_id)
                )
                conn.commit()
                return cursor.rowcount > 0
                    
        except sqlite3.Error as e:
            self.logger.exception("カテゴリー名変更エラー", exc_info=e)
            return False

    def delete_parent_category(self, name: str, group_id: int) -> bool:
        """
        親カテゴリーを削除する
        
        Args:
            name (str): カテゴリー名
            group_id (int): グループID
            
        Returns:
            bool: 削除に成功した場合はTrue、失敗した場合はFalse
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # カテゴリーIDを取得
                cursor.execute(
                    """
                    SELECT category_id
                    FROM categories
                    WHERE name = ? AND group_id = ?
                    """,
                    (name, group_id)
                )
                category_id = cursor.fetchone()
                
                if category_id:
                    # 関連するスキルを削除
                    cursor.execute(
                        """
                        DELETE FROM skills 
                        WHERE parent_id = ?
                        """,
                        (category_id[0],)
                    )
                    
                    # カテゴリーを削除
                    cursor.execute(
                        """
                        DELETE FROM categories
                        WHERE category_id = ?
                        """,
                        (category_id[0],)
                    )
                    
                    conn.commit()
                    return True
                    
                return False
                
        except sqlite3.Error as e:
            self.logger.exception("カテゴリー削除エラー", exc_info=e)
            return False

    # 以前のメソッド名との互換性のために別名を提供
    def get_categories_by_group(self, group_name: str) -> list[str]:
        """
        グループ名からカテゴリーを取得する（互換性のため）
        """
        group_id = self.get_group_id_by_name(group_name)
        if group_id is not None:
            return self.get_parent_categories_by_group(group_id)
        return []

    def add_category(self, name: str, group_name: str) -> bool:
        """
        グループ名でカテゴリーを追加する（互換性のため）
        """
        group_id = self.get_group_id_by_name(group_name)
        if group_id is not None:
            return self.add_parent_category(name, group_id)
        return False

    def rename_category(self, old_name: str, new_name: str, group_name: str) -> bool:
        """
        グループ名でカテゴリーを変更する（互換性のため）
        """
        group_id = self.get_group_id_by_name(group_name)
        if group_id is not None:
            return self.rename_parent_category(old_name, new_name, group_id)
        return False

    def delete_category(self, name: str, group_name: str) -> bool:
        """
        グループ名でカテゴリーを削除する（互換性のため）
        """
        group_id = self.get_group_id_by_name(group_name)
        if group_id is not None:
            return self.delete_parent_category(name, group_id)
        return False
