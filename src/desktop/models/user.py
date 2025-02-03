from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    """ユーザーモデル"""
    id: int
    employee_id: str
    name: str
    group_id: int | None
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_dict(data: dict) -> 'User':
        """辞書からUserオブジェクトを作成"""
        return User(
            id=data.get('id'),
            employee_id=data.get('employee_id'),
            name=data.get('name'),
            group_id=data.get('group_id'),
            created_at=datetime.fromisoformat(data.get('created_at')) if data.get('created_at') else datetime.now(),
            updated_at=datetime.fromisoformat(data.get('updated_at')) if data.get('updated_at') else datetime.now()
        )