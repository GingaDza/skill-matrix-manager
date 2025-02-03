from dataclasses import dataclass
from datetime import datetime

@dataclass
class Skill:
    """スキルモデル"""
    id: int
    category_id: int
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_dict(data: dict) -> 'Skill':
        """辞書からSkillオブジェクトを作成"""
        return Skill(
            id=data.get('id'),
            category_id=data.get('category_id'),
            name=data.get('name'),
            description=data.get('description'),
            created_at=datetime.fromisoformat(data.get('created_at')) if data.get('created_at') else datetime.now(),
            updated_at=datetime.fromisoformat(data.get('updated_at')) if data.get('updated_at') else datetime.now()
        )