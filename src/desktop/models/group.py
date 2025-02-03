from dataclasses import dataclass
from datetime import datetime

@dataclass
class Group:
    """グループモデル"""
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_dict(data: dict) -> 'Group':
        """辞書からGroupオブジェクトを作成"""
        return Group(
            id=data.get('id'),
            name=data.get('name'),
            created_at=datetime.fromisoformat(data.get('created_at')) if data.get('created_at') else datetime.now(),
            updated_at=datetime.fromisoformat(data.get('updated_at')) if data.get('updated_at') else datetime.now()
        )