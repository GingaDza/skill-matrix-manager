import pytest
from datetime import datetime
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base
from src.app.models.base import TimestampMixin

def test_timestamp_mixin(db: Session):
    """タイムスタンプミックスインのテスト"""
    TestBase = declarative_base()

    class TestTimeStampModel(TestBase, TimestampMixin):
        __tablename__ = "test_timestamp"
        id = Column(Integer, primary_key=True)
        name = Column(String)

    # テーブルを作成
    TestBase.metadata.create_all(db.bind)

    try:
        # インスタンスを作成してDBに保存
        instance = TestTimeStampModel(name="test")
        db.add(instance)
        db.flush()

        # 検証
        assert isinstance(instance.created_at, datetime)
        assert isinstance(instance.updated_at, datetime)
        
        # 更新前の時刻を保存
        original_created_at = instance.created_at
        original_updated_at = instance.updated_at

        # 更新
        instance.name = "updated"
        db.flush()

        # 更新後の検証
        assert instance.created_at == original_created_at  # created_atは変更されない
        assert instance.updated_at > original_updated_at  # updated_atは更新される

    finally:
        # クリーンアップ
        TestBase.metadata.drop_all(db.bind)