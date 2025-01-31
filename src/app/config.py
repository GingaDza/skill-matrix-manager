# src/app/config.py
from datetime import datetime, timedelta
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """アプリケーション設定"""
    # データベース設定
    DATABASE_URL: str = "sqlite:///./skill_matrix.db"
    TEST_DATABASE_URL: str = "sqlite:///./test.db"
    
    # JWT設定
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # テスト用設定
    NOW: Optional[datetime] = None

    class Config:
        env_file = ".env"

    def get_current_time(self) -> datetime:
        """
        現在時刻を取得
        テスト時は NOW が設定されていればその値を返す
        """
        return self.NOW or datetime.utcnow()

    def get_token_expiration(self) -> datetime:
        """
        トークンの有効期限を取得
        """
        return self.get_current_time() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

settings = Settings()  # インスタンスを作成して設定を読み込む