"""カテゴリー操作のミックスイン"""
import sqlite3

class CategoryManagerMixin:
    """カテゴリー操作を提供するミックスイン"""

    def get_categories_by_group(self, group_name: str) -> list[str]:
        """
        グループに属するカテゴリーの一覧を取得する
        
        Args:
            group_name (str): グループ名
            
        Returns:
            list[str]: カテゴリー名のリスト
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    """
                    SELECT c.name
                    FROM categories c
                    JOIN groups g ON c.group_id = g.group_id
                    WHERE g.name = ?
                    ORDER BY c.name
                    """,
                    (group_name,)
                )
                
                return [row[0] for row in cursor.fetchall()]
                
        except sqlite3.Error as e:
            self.logger.exception("カテゴリー取得エラー", exc_info=e)
            return []

    def add_category(self, name: str, group_name: str) -> bool:
        """
        カテゴリーを追加する
        
        Args:
            name (str): カテゴリー名
            group_name (str): グループ名
            
        Returns:
            bool: 追加に成功した場合はTrue、失敗した場合はFalse
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # グループIDを取得
                cursor.execute(
                    "SELECT group_id FROM groups WHERE name = ?",
                    (group_name,)
                )
                group_id = cursor.fetchone()
                
                if group_id:
                    cursor.execute(
                        """
                        INSERT INTO categories (name, group_id, created_at, updated_at)
                        VALUES (?, ?, ?, ?)
                        """,
                        (name, group_id[0], self.current_time, self.current_time)
                    )
                    conn.commit()
                    return True
                    
                return False
                
        except sqlite3.Error as e:
            self.logger.exception("カテゴリー追加エラー", exc_info=e)
            return False

    def rename_category(self, old_name: str, new_name: str, group_name: str) -> bool:
        """
        カテゴリー名を変更する
        
        Args:
            old_name (str): 現在のカテゴリー名
            new_name (str): 新しいカテゴリー名
            group_name (str): グループ名
            
        Returns:
            bool: 変更に成功した場合はTrue、失敗した場合はFalse
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # グループIDを取得
                cursor.execute(
                    "SELECT group_id FROM groups WHERE name = ?",
                    (group_name,)
                )
                group_id = cursor.fetchone()
                
                if group_id:
                    cursor.execute(
                        """
                        UPDATE categories
                        SET name = ?, updated_at = ?
                        WHERE name = ? AND group_id = ?
                        """,
                        (new_name, self.current_time, old_name, group_id[0])
                    )
                    conn.commit()
                    return cursor.rowcount > 0
                    
                return False
                
        except sqlite3.Error as e:
            self.logger.exception("カテゴリー名変更エラー", exc_info=e)
            return False

    def delete_category(self, name: str, group_name: str) -> bool:
        """
        カテゴリーを削除する
        
        Args:
            name (str): カテゴリー名
            group_name (str): グループ名
            
        Returns:
            bool: 削除に成功した場合はTrue、失敗した場合はFalse
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # グループIDを取得
                cursor.execute(
                    "SELECT group_id FROM groups WHERE name = ?",
                    (group_name,)
                )
                group_id = cursor.fetchone()
                
                if group_id:
                    # カテゴリーIDを取得
                    cursor.execute(
                        """
                        SELECT category_id
                        FROM categories
                        WHERE name = ? AND group_id = ?
                        """,
                        (name, group_id[0])
                    )
                    category_id = cursor.fetchone()
                    
                    if category_id:
                        # 関連するスキルを削除
                        cursor.execute(
                            "DELETE FROM skills WHERE parent_id = ?",
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
