# tests/test_user.py
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from src.app.models import Base, User, Skill, Category, SkillAssessment, ProficiencyLevel

class TestUser(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def test_create_user(self):
        user = User(
            username="johndoe",
            email="john@example.com",
            full_name="John Doe"
        )
        self.session.add(user)
        self.session.commit()

        saved_user = self.session.query(User).first()
        self.assertEqual(saved_user.username, "johndoe")
        self.assertEqual(saved_user.email, "john@example.com")
        self.assertTrue(saved_user.is_active)
        self.assertFalse(saved_user.is_admin)

    def test_user_skill_assessment(self):
        # ユーザーの作成
        user = User(
            username="johndoe",
            email="john@example.com",
            full_name="John Doe"
        )
        self.session.add(user)

        # カテゴリとスキルの作成
        category = Category(name="Programming")
        self.session.add(category)
        self.session.flush()

        skill = Skill(
            name="Python",
            description="プログラミング言語",
            category_id=category.id
        )
        self.session.add(skill)
        self.session.flush()

        # スキル評価の作成
        assessment = SkillAssessment(
            user_id=user.id,
            skill_id=skill.id,
            proficiency_level=ProficiencyLevel.ADVANCED.value,
            notes="良好な進捗"
        )
        self.session.add(assessment)
        self.session.commit()

        # 検証
        saved_assessment = self.session.query(SkillAssessment).first()
        self.assertEqual(saved_assessment.user.username, "johndoe")
        self.assertEqual(saved_assessment.skill.name, "Python")
        self.assertEqual(saved_assessment.proficiency_level, ProficiencyLevel.ADVANCED.value)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)
        self.session.close()