# src/app/routes/__init__.py
from fastapi import APIRouter, Depends
from . import auth, category, skill, skill_assessment
from ..utils.deps import get_current_user

api_router = APIRouter()

# プロテクテッドルートを最初に定義
@api_router.get("/protected-route")
async def protected_route(current_user = Depends(get_current_user)):
    return {"message": "Protected route accessed successfully"}

# 各ルーターをマウント
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(category.router, prefix="/categories", tags=["categories"])
api_router.include_router(skill.router, prefix="/skills", tags=["skills"])
api_router.include_router(
    skill_assessment.router,
    prefix="/skill-assessments",
    tags=["skill-assessments"]
)