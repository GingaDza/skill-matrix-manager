"""データベース操作の例外定義"""

class DatabaseError(Exception):
    """データベース操作の基本例外"""
    pass

class EntityNotFoundError(DatabaseError):
    """エンティティが見つからない場合の例外"""
    pass

class DuplicateEntityError(DatabaseError):
    """エンティティが重複している場合の例外"""
    pass
