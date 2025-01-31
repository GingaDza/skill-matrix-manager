# src/app/utils/deps.py
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from ..database import SessionLocal
from ..models.user import User
from ..config import settings

# データベースセッション依存関係
def get_db() -> Generator[Session, None, None]:
    """
    データベースセッションの依存関係を提供する
    FastAPIのDependsで使用される
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# OAuth2認証スキーム
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# 現在のユーザー取得の依存関係
async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    JWTトークンから現在のユーザーを取得する
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user