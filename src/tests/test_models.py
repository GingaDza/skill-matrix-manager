# tests/test_models.py
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.models import Base, Category, Skill

class TestModels(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def test_category_hierarchy(self):
        # 親カテゴリの作成
        programming = Category(name="Programming")
        self.session.add(programming)
        self.session.flush()

        # 子カテゴリの作成
        python = Category(name="Python", parent_id=programming.id)
        self.session.add(python)
        self.session.flush()

        # スキルの作成
        django = Skill(
            name="Django",
            description="Webフレームワーク",
            category_id=python.id
        )
        self.session.add(django)
        self.session.commit()

        # 検証
        saved_python = self.session.query(Category).filter_by(name="Python").first()
        self.assertEqual(saved_python.parent.name, "Programming")
        self.assertEqual(saved_python.skills[0].name, "Django")

    def test_skill_creation(self):
        # カテゴリの作成
        category = Category(name="Programming")
        self.session.add(category)
        self.session.commit()

        # スキルの作成
        skill = Skill(
            name="Python",
            description="プログラミング言語",
            category_id=category.id
        )
        self.session.add(skill)
        self.session.commit()

        # 検証
        saved_skill = self.session.query(Skill).first()
        self.assertEqual(saved_skill.name, "Python")
        self.assertEqual(saved_skill.category.name, "Programming")

    def tearDown(self):
        Base.metadata.drop_all(self.engine)
        self.session.close()