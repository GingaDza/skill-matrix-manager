"""グループ管理クラス"""
from typing import List
import sqlite3
from ..base_manager import BaseManager

class GroupManager(BaseManager):
    """グループ管理クラス"""

    def get_groups(self) -> List[str]:
        """グループ一覧を取得"""
        try:
            rows = self._execute("SELECT name FROM groups ORDER BY name")
            return [row[0] for row in rows]
        except Exception as e:
            self.logger.exception("グループ一覧の取得に失敗しました")
            raise RuntimeError(f"グループ一覧の取得に失敗しました: {str(e)}")

    def add_group(self, name: str):
        """グループを追加"""
        try:
            self._execute(
                "INSERT INTO groups (name) VALUES (?)",
                (name,),
                commit=True
            )
        except sqlite3.IntegrityError:
            raise ValueError(f"グループ '{name}' は既に存在します")
        except Exception as e:
            self.logger.exception("グループの追加に失敗しました")
            raise RuntimeError(f"グループの追加に失敗しました: {str(e)}")
    
    # ... 他のグループ関連メソッド
