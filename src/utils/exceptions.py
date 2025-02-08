"""カスタム例外クラス"""
class SkillMatrixError(Exception):
    """アプリケーション固有の基本例外クラス"""
    pass

class DatabaseError(SkillMatrixError):
    """データベース操作に関連する例外"""
    pass

class ValidationError(SkillMatrixError):
    """データ検証に関連する例外"""
    pass

class NotFoundError(SkillMatrixError):
    """リソースが見つからない場合の例外"""
    pass

class DuplicateError(SkillMatrixError):
    """リソースが重複している場合の例外"""
    pass
