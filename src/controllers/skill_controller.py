import logging
from typing import List
from src.desktop.models.skill import Skill
from src.desktop.managers.skill_manager import SkillManager
from src.desktop.utils.time_utils import TimeProvider

logger = logging.getLogger(__name__)

class SkillController:
    """スキルコントローラー"""
    
    def __init__(self, skill_manager: SkillManager):
        self.skill_manager = skill_manager
        self.current_time = TimeProvider.get_current_time()
        
    def create_skill(self, category_id: int, name: str, description: str = None) -> Skill:
        """スキルを作成"""
        try:
            skill = self.skill_manager.create_skill(category_id, name, description)
            logger.debug(f"{self.current_time} - Created skill: {name}")
            return skill
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to create skill: {str(e)}")
            raise
            
    def get_skill(self, skill_id: int) -> Skill:
        """スキルを取得"""
        try:
            skill = self.skill_manager.get_skill(skill_id)
            logger.debug(f"{self.current_time} - Retrieved skill: {skill.name}")
            return skill
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get skill: {str(e)}")
            raise
            
    def get_all_skills(self) -> List[Skill]:
        """全スキルを取得"""
        try:
            skills = self.skill_manager.get_all_skills()
            logger.debug(f"{self.current_time} - Retrieved {len(skills)} skills")
            return skills
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get all skills: {str(e)}")
            raise
            
    def get_skills_by_category(self, category_id: int) -> List[Skill]:
        """カテゴリーに属するスキルを取得"""
        try:
            skills = self.skill_manager.get_skills_by_category(category_id)
            logger.debug(f"{self.current_time} - Retrieved {len(skills)} skills for category {category_id}")
            return skills
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get skills by category: {str(e)}")
            raise
            
    def update_skill(self, skill_id: int, category_id: int = None, name: str = None, description: str = None) -> Skill:
        """スキル情報を更新"""
        try:
            skill = self.skill_manager.update_skill(skill_id, category_id, name, description)
            logger.debug(f"{self.current_time} - Updated skill: {skill.name}")
            return skill
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to update skill: {str(e)}")
            raise
            
    def delete_skill(self, skill_id: int) -> bool:
        """スキルを削除"""
        try:
            success = self.skill_manager.delete_skill(skill_id)
            logger.debug(f"{self.current_time} - Deleted skill: {skill_id}")
            return success
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to delete skill: {str(e)}")
            raise