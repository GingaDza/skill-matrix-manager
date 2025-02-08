"""スキル操作のミックスイン"""
import sqlite3

class SkillManagerMixin:
    """スキル操作を提供するミックスイン"""

    def add_skill(self, parent_name: str, skill_name: str) -> bool:
        """
        スキルを追加する
        
        Args:
            parent_name (str): 親カテゴリー名
            skill_name (str): スキル名
            
        Returns:
            bool: 追加に成功した場合はTrue、失敗した場合はFalse
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # 親カテゴリーのIDを取得
                cursor.execute(
                    "SELECT category_id FROM categories WHERE name = ?",
                    (parent_name,)
                )
                parent_id = cursor.fetchone()
                
                if parent_id:
                    cursor.execute(
                        """
                        INSERT INTO skills (name, parent_id, created_at, updated_at)
                        VALUES (?, ?, ?, ?)
                        """,
                        (skill_name, parent_id[0], self.current_time, self.current_time)
                    )
                    conn.commit()
                    return True
                    
                return False
                
        except sqlite3.Error as e:
            self.logger.exception("スキル追加エラー", exc_info=e)
            return False

    def get_skills_by_parent(self, parent_name: str) -> list[str]:
        """
        親カテゴリーに属するスキルの一覧を取得する
        
        Args:
            parent_name (str): 親カテゴリー名
            
        Returns:
            list[str]: スキル名のリスト
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    """
                    SELECT s.name
                    FROM skills s
                    JOIN categories c ON s.parent_id = c.category_id
                    WHERE c.name = ?
                    ORDER BY s.name
                    """,
                    (parent_name,)
                )
                
                return [row[0] for row in cursor.fetchall()]
                
        except sqlite3.Error as e:
            self.logger.exception("スキル取得エラー", exc_info=e)
            return []

    def rename_skill(self, old_name: str, new_name: str) -> bool:
        """
        スキル名を変更する
        
        Args:
            old_name (str): 現在のスキル名
            new_name (str): 新しいスキル名
            
        Returns:
            bool: 変更に成功した場合はTrue、失敗した場合はFalse
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE skills
                    SET name = ?, updated_at = ?
                    WHERE name = ?
                    """,
                    (new_name, self.current_time, old_name)
                )
                conn.commit()
                return cursor.rowcount > 0
                
        except sqlite3.Error as e:
            self.logger.exception("スキル名変更エラー", exc_info=e)
            return False

    def delete_skill(self, skill_name: str) -> bool:
        """
        スキルを削除する
        
        Args:
            skill_name (str): スキル名
            
        Returns:
            bool: 削除に成功した場合はTrue、失敗した場合はFalse
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # 関連する評価を削除
                cursor.execute(
                    """
                    DELETE FROM evaluations
                    WHERE skill_id IN (
                        SELECT skill_id
                        FROM skills
                        WHERE name = ?
                    )
                    """,
                    (skill_name,)
                )
                
                # スキルを削除
                cursor.execute(
                    "DELETE FROM skills WHERE name = ?",
                    (skill_name,)
                )
                
                conn.commit()
                return cursor.rowcount > 0
                
        except sqlite3.Error as e:
            self.logger.exception("スキル削除エラー", exc_info=e)
            return False
