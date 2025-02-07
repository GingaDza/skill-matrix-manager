import logging
from typing import List
from datetime import datetime
from src.desktop.models.skill import Skill
from src.desktop.database.database import Database
from src.desktop.utils.time_utils import TimeProvider

logger = logging.getLogger(__name__)

class SkillManager:
    """スキル管理クラス"""
    
    def __init__(self, database: Database):
        self.db = database
        self.current_time = TimeProvider.get_current_time()
        
    def create_skill(self, category_id: int, name: str, description: str = None) -> Skill:
        """スキルを作成"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                current_time = datetime.now().isoformat()
                
                cursor.execute('''
                    INSERT INTO skills (category_id, name, description, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (category_id, name, description, current_time, current_time))
                
                skill_id = cursor.lastrowid
                conn.commit()
                
                return Skill(
                    id=skill_id,
                    category_id=category_id,
                    name=name,
                    description=description,
                    created_at=datetime.fromisoformat(current_time),
                    updated_at=datetime.fromisoformat(current_time)
                )
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to create skill: {str(e)}")
            raise
            
    def get_skill(self, skill_id: int) -> Skill:
        """スキルを取得"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT * FROM skills WHERE id = ?', (skill_id,))
                row = cursor.fetchone()
                
                if row:
                    return Skill(
                        id=row[0],
                        category_id=row[1],
                        name=row[2],
                        description=row[3],
                        created_at=datetime.fromisoformat(row[4]),
                        updated_at=datetime.fromisoformat(row[5])
                    )
                return None
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get skill: {str(e)}")
            raise
            
    def get_all_skills(self) -> List[Skill]:
        """全スキルを取得"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM skills 
                    ORDER BY category_id, name
                ''')
                rows = cursor.fetchall()
                
                return [
                    Skill(
                        id=row[0],
                        category_id=row[1],
                        name=row[2],
                        description=row[3],
                        created_at=datetime.fromisoformat(row[4]),
                        updated_at=datetime.fromisoformat(row[5])
                    )
                    for row in rows
                ]
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get all skills: {str(e)}")
            raise
            
    def get_skills_by_category(self, category_id: int) -> List[Skill]:
        """カテゴリーに属するスキルを取得"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM skills 
                    WHERE category_id = ? 
                    ORDER BY name
                ''', (category_id,))
                rows = cursor.fetchall()
                
                return [
                    Skill(
                        id=row[0],
                        category_id=row[1],
                        name=row[2],
                        description=row[3],
                        created_at=datetime.fromisoformat(row[4]),
                        updated_at=datetime.fromisoformat(row[5])
                    )
                    for row in rows
                ]
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to get skills by category: {str(e)}")
            raise
            
    def update_skill(self, skill_id: int, category_id: int = None, name: str = None, description: str = None) -> Skill:
        """スキル情報を更新"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                current_time = datetime.now().isoformat()
                
                # 現在のスキル情報を取得
                cursor.execute('SELECT * FROM skills WHERE id = ?', (skill_id,))
                row = cursor.fetchone()
                
                if not row:
                    raise ValueError(f"Skill not found: {skill_id}")
                    
                # 更新するフィールドを設定
                update_category_id = category_id if category_id is not None else row[1]
                update_name = name if name is not None else row[2]
                update_description = description if description is not None else row[3]
                
                # 更新を実行
                cursor.execute('''
                    UPDATE skills
                    SET category_id = ?, name = ?, description = ?, updated_at = ?
                    WHERE id = ?
                ''', (update_category_id, update_name, update_description, current_time, skill_id))
                
                conn.commit()
                
                return Skill(
                    id=skill_id,
                    category_id=update_category_id,
                    name=update_name,
                    description=update_description,
                    created_at=datetime.fromisoformat(row[4]),
                    updated_at=datetime.fromisoformat(current_time)
                )
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to update skill: {str(e)}")
            raise
            
    def delete_skill(self, skill_id: int) -> bool:
        """スキルを削除"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                # 関連するユーザースキルを削除
                cursor.execute('DELETE FROM user_skills WHERE skill_id = ?', (skill_id,))
                
                # スキルを削除
                cursor.execute('DELETE FROM skills WHERE id = ?', (skill_id,))
                conn.commit()
                
                return cursor.rowcount > 0
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to delete skill: {str(e)}")
            raise