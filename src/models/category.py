from datetime import datetime

class Category:
    """カテゴリーモデル"""
    
    def __init__(self, id=None, name="", description="", parent_id=None):
        self.id = id
        self.name = name
        self.description = description
        self.parent_id = parent_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.skills = []  # このカテゴリーに属するスキル
        self.children = []  # 子カテゴリー

    def add_skill(self, skill):
        """スキルを追加"""
        self.skills.append(skill)

    def add_child(self, category):
        """子カテゴリーを追加"""
        self.children.append(category)

    def remove_child(self, category):
        """子カテゴリーを削除"""
        self.children.remove(category)

    def to_dict(self):
        """辞書形式でデータを取得"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
