# tests/test_base.py
import unittest
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker
from src.app.models.base import Base, TimestampMixin

class TestBase(unittest.TestCase):
    def setUp(self):
        """テスト用データベースの設定"""
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def test_timestamp_mixin(self):
        """TimestampMixinのテスト"""
        # テスト用のモデルクラスを作成
        class TestModel(Base, TimestampMixin):
            __tablename__ = 'test_models'
            id = Column(Integer, primary_key=True)

        # テーブルの作成
        TestModel.__table__.create(bind=self.engine)

        # モデルのインスタンスを作成
        test_instance = TestModel()
        self.session.add(test_instance)
        self.session.commit()

        # created_atとupdated_atが設定されていることを確認
        self.assertIsNotNone(test_instance.created_at)
        self.assertIsNotNone(test_instance.updated_at)

    def tearDown(self):
        """テスト後のクリーンアップ"""
        self.session.close()