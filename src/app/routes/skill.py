# src/app/routes/skill.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models import Skill
from ..schemas.skill import SkillCreate, SkillResponse
from ..utils.deps import get_db, get_current_user

router = APIRouter()

# src/app/routes/skill.py
@router.post("/", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
def create_skill(
    skill: SkillCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_skill = Skill(**skill.model_dump())  # dict()をmodel_dump()に変更
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill