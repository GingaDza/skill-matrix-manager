# tests/utils/test_db.py
def test_timestamp_mixin(db):
    """TimestampMixinのテスト"""
    class TestTimeStampModel(Base, TimestampMixin):
        __tablename__ = "test_timestamp"
        id = Column(Integer, primary_key=True)
        name = Column(String)

    # テーブルを作成
    TestTimeStampModel.__table__.create(db.bind)

    instance = TestTimeStampModel(name="test")
    db.add(instance)
    db.commit()

    assert isinstance(instance.created_at, datetime)
    assert isinstance(instance.updated_at, datetime)

    # クリーンアップ
    TestTimeStampModel.__table__.drop(db.bind)