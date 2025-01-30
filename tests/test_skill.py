# tests/test_skill.py
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.models.base import Base
from src.app.models.skill import Skill

class TestSkill(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def test_create_skill(self):
        skill = Skill(name="Python", description="プログラミング言語")
        self.session.add(skill)
        self.session.commit()

        saved_skill = self.session.query(Skill).first()
        self.assertEqual(saved_skill.name, "Python")
        self.assertEqual(saved_skill.description, "プログラミング言語")
        self.assertIsNotNone(saved_skill.created_at)
        self.assertIsNotNone(saved_skill.updated_at)

    def tearDown(self):
        self.session.close()