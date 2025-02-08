"""データベースインターフェース定義"""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

class IDataManager(ABC):
    """データ管理インターフェース"""
    
    @abstractmethod
    def get_group_id_by_name(self, name: str) -> Optional[int]:
        """グループ名からIDを取得"""
        pass
    
    @abstractmethod
    def get_category_id_by_name(self, name: str, group_name: str) -> Optional[int]:
        """カテゴリー名からIDを取得"""
        pass
