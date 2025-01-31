# tests/test_skill.py
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.models import Base, Category, Skill

class TestSkill(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        # テストデータのセットアップ
        self.category = Category(name="Programming")
        self.session.add(self.category)
        self.session.commit()

    def test_create_skill(self):
        skill = Skill(
            name="Python",
            description="プログラミング言語",
            category_id=self.category.id
        )
        self.session.add(skill)
        self.session.commit()

        saved_skill = self.session.query(Skill).first()
        self.assertEqual(saved_skill.name, "Python")
        self.assertEqual(saved_skill.description, "プログラミング言語")
        self.assertEqual(saved_skill.category_id, self.category.id)

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)