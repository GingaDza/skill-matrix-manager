# src/app/routes/category.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models import Category
from ..schemas.category import CategoryCreate, CategoryResponse
from ..utils.deps import get_db, get_current_user

router = APIRouter()

# src/app/routes/category.py
@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_category = Category(**category.model_dump())  # dict()をmodel_dump()に変更
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category