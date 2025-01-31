# tests/test_base.py
import pytest
from datetime import datetime
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base
from src.app.models.base import TimestampMixin

# tests/test_base.py
def test_timestamp_mixin(db):
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

    finally:
        # クリーンアップ
        TestBase.metadata.drop_all(db.bind)