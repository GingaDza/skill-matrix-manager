"""スキル管理クラス"""
from typing import List, Dict, Any, Optional
import sqlite3
from ..base_manager import BaseManager

class SkillManager(BaseManager):
    """スキル管理クラス"""

    def get_skills(self, category_name: str, group_name: str) -> List[Dict[str, Any]]:
        """スキル一覧を取得"""
        try:
            rows = self._execute("""
                SELECT s.name, s.description, s.min_level, s.max_level
                FROM skills s
                JOIN categories c ON s.category_id = c.id
                JOIN groups g ON c.group_id = g.id
                WHERE c.name = ? AND g.name = ?
                ORDER BY s.name
            """, (category_name, group_name))
            return [
                {
                    'name': row[0],
                    'description': row[1],
                    'min_level': row[2],
                    'max_level': row[3]
                }
                for row in rows
            ]
        except Exception as e:
            self.logger.exception("スキル一覧の取得に失敗しました")
            raise RuntimeError(f"スキル一覧の取得に失敗しました: {str(e)}")
    
    # ... 他のスキル関連メソッド
