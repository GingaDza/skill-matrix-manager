"""データベース管理クラス"""
import sqlite3
import logging
from typing import List, Optional, Dict, Any

class DatabaseManager:
    """データベース管理クラス"""
    
    def __init__(self, db_path: str = "skill_matrix.db"):
        """初期化"""
        self.logger = logging.getLogger(__name__)
        self._db_path = db_path
        self._init_db()
    
    # ... (_init_db と他のメソッドは同じ)
    
    def get_categories(self, group_name: str) -> List[Dict[str, Any]]:
        """カテゴリー一覧を取得"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT c.name, p.name
                    FROM categories c
                    JOIN groups g ON c.group_id = g.id
                    LEFT JOIN categories p ON c.parent_id = p.id
                    WHERE g.name = ?
                    ORDER BY c.name
                    """,
                    (group_name,)
                )
                return [
                    {
                        'name': row[0],
                        'parent_name': row[1]
                    }
                    for row in cursor.fetchall()
                ]
        except Exception as e:
            self.logger.exception("カテゴリー一覧の取得に失敗しました")
            raise RuntimeError(f"カテゴリー一覧の取得に失敗しました: {str(e)}")

    def get_category(self, name: str, group_name: str) -> Optional[Dict[str, Any]]:
        """カテゴリー情報を取得"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT c.name, p.name
                    FROM categories c
                    JOIN groups g ON c.group_id = g.id
                    LEFT JOIN categories p ON c.parent_id = p.id
                    WHERE c.name = ? AND g.name = ?
                    """,
                    (name, group_name)
                )
                row = cursor.fetchone()
                return {
                    'name': row[0],
                    'parent_name': row[1]
                } if row else None
        except Exception as e:
            self.logger.exception("カテゴリー情報の取得に失敗しました")
            raise RuntimeError(f"カテゴリー情報の取得に失敗しました: {str(e)}")

    def add_category(self, name: str, group_name: str, parent_name: Optional[str] = None):
        """カテゴリーを追加"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                
                # グループIDを取得
                cursor.execute(
                    "SELECT id FROM groups WHERE name = ?",
                    (group_name,)
                )
                group_id = cursor.fetchone()
                if not group_id:
                    raise ValueError(f"グループ '{group_name}' が見つかりません")
                
                # 親カテゴリーIDを取得（指定されている場合）
                parent_id = None
                if parent_name:
                    cursor.execute(
                        """
                        SELECT c.id 
                        FROM categories c
                        JOIN groups g ON c.group_id = g.id
                        WHERE c.name = ? AND g.name = ?
                        """,
                        (parent_name, group_name)
                    )
                    parent_row = cursor.fetchone()
                    if not parent_row:
                        raise ValueError(f"親カテゴリー '{parent_name}' が見つかりません")
                    parent_id = parent_row[0]
                
                # カテゴリーを追加
                cursor.execute(
                    """
                    INSERT INTO categories (name, group_id, parent_id)
                    VALUES (?, ?, ?)
                    """,
                    (name, group_id[0], parent_id)
                )
                conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"カテゴリー '{name}' は既に存在します")
        except Exception as e:
            self.logger.exception("カテゴリーの追加に失敗しました")
            raise RuntimeError(f"カテゴリーの追加に失敗しました: {str(e)}")

    # ... (他のメソッドは同じ)
