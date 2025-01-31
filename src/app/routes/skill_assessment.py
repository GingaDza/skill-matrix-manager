from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models import User
from ..schemas.auth import UserCreate, Token, UserLogin
from ..utils.deps import get_db
from ..utils.security import get_password_hash, create_access_token, verify_password

router = APIRouter()

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # 既存ユーザーチェック
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password),
        is_admin=user.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # アクセストークンを生成
    access_token = create_access_token(
        data={"sub": db_user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}