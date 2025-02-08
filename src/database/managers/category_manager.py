"""カテゴリー管理クラス"""
from typing import List, Dict, Any, Optional
import sqlite3
from ..base_manager import BaseManager

class CategoryManager(BaseManager):
    """カテゴリー管理クラス"""

    def get_categories(self, group_name: str) -> List[Dict[str, Any]]:
        """カテゴリー一覧を取得"""
        try:
            rows = self._execute("""
                SELECT c.name, p.name
                FROM categories c
                JOIN groups g ON c.group_id = g.id
                LEFT JOIN categories p ON c.parent_id = p.id
                WHERE g.name = ?
                ORDER BY c.name
            """, (group_name,))
            return [
                {
                    'name': row[0],
                    'parent_name': row[1]
                }
                for row in rows
            ]
        except Exception as e:
            self.logger.exception("カテゴリー一覧の取得に失敗しました")
            raise RuntimeError(f"カテゴリー一覧の取得に失敗しました: {str(e)}")
    
    # ... 他のカテゴリー関連メソッド
