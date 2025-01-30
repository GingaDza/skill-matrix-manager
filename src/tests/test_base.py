# tests/test_base.py
import unittest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from src.app.models.base import Base, TimestampMixin

class SimpleModel(Base, TimestampMixin):
    __tablename__ = 'simple_models'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

class TestBase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def test_timestamp_mixin(self):
        model = SimpleModel(name="test")
        self.session.add(model)
        self.session.commit()

        self.assertIsNotNone(model.created_at)
        self.assertIsNotNone(model.updated_at)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)
        self.session.close()