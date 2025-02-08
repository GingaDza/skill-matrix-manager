"""データベースマネージャークラス"""
from .base_manager import BaseManagerMixin
from .group_manager import GroupManagerMixin
from .category_manager import CategoryManagerMixin
from .skill_manager import SkillManagerMixin
from .evaluation_manager import EvaluationManagerMixin

class DatabaseManager(
    BaseManagerMixin,
    GroupManagerMixin,
    CategoryManagerMixin,
    SkillManagerMixin,
    EvaluationManagerMixin
):
    """データベース操作を統合するクラス"""
    pass
