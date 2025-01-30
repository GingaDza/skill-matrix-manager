# tests/test_category.py
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.models import Base, Category

class TestCategory(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def test_create_category(self):
        category = Category(name="Programming")
        self.session.add(category)
        self.session.commit()

        saved_category = self.session.query(Category).first()
        self.assertEqual(saved_category.name, "Programming")
        self.assertIsNotNone(saved_category.created_at)
        self.assertIsNotNone(saved_category.updated_at)

    def test_create_subcategory(self):
        parent = Category(name="Programming")
        self.session.add(parent)
        self.session.commit()

        child = Category(name="Python", parent_id=parent.id)
        self.session.add(child)
        self.session.commit()

        saved_child = self.session.query(Category).filter_by(name="Python").first()
        self.assertEqual(saved_child.parent_id, parent.id)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)
        self.session.close()