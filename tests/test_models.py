# tests/test_models.py
from datetime import datetime
from sqlalchemy.orm import Session
from src.app.models.skill_assessment import SkillAssessment
from src.app.models.enums import ProficiencyLevel  # SkillLevel から変更

def test_skill_assessment_create(db: Session):
    """スキルアセスメントの作成テスト"""
    assessment = SkillAssessment(
        user_id=1,
        skill_id=1,
        proficiency_level=ProficiencyLevel.BEGINNER
    )
    
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    
    assert assessment.id is not None
    assert assessment.user_id == 1
    assert assessment.skill_id == 1
    assert assessment.proficiency_level == ProficiencyLevel.BEGINNER
    assert isinstance(assessment.created_at, datetime)
    assert isinstance(assessment.updated_at, datetime)