import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.app.models import Base, User, Skill, Category, SkillAssessment
from src.app.models.enums import ProficiencyLevel  # SkillLevel から ProficiencyLevel に変更
from src.app.schemas.auth import UserCreate, UserLogin
from src.app.utils.security import get_password_hash

def test_create_user(db: Session):
    """ユーザー作成のテスト"""
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123"
    )
    
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password)
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    assert db_user.id is not None
    assert db_user.username == "testuser"
    assert db_user.email == "test@example.com"
    assert db_user.hashed_password != "password123"
    assert isinstance(db_user.created_at, datetime)
    assert isinstance(db_user.updated_at, datetime)

def test_create_duplicate_username(db: Session):
    """重複ユーザー名のテスト"""
    # 最初のユーザーを作成
    user1 = User(
        username="duplicate",
        email="user1@example.com",
        hashed_password=get_password_hash("password123")
    )
    db.add(user1)
    db.commit()
    
    # 同じユーザー名で2人目のユーザーを作成
    user2 = User(
        username="duplicate",
        email="user2@example.com",
        hashed_password=get_password_hash("password123")
    )
    db.add(user2)
    
    # 重複エラーが発生することを確認
    with pytest.raises(IntegrityError):
        db.commit()

def test_create_duplicate_email(db: Session):
    """重複メールアドレスのテスト"""
    # 最初のユーザーを作成
    user1 = User(
        username="user1",
        email="duplicate@example.com",
        hashed_password=get_password_hash("password123")
    )
    db.add(user1)
    db.commit()
    
    # 同じメールアドレスで2人目のユーザーを作成
    user2 = User(
        username="user2",
        email="duplicate@example.com",
        hashed_password=get_password_hash("password123")
    )
    db.add(user2)
    
    # 重複エラーが発生することを確認
    with pytest.raises(IntegrityError):
        db.commit()

def test_user_skill_assessment(db: Session):
    """ユーザーのスキルアセスメントのテスト"""
    # ユーザーを作成
    user = User(
        username="skilluser",
        email="skill@example.com",
        hashed_password=get_password_hash("password123")
    )
    db.add(user)
    
    # カテゴリーを作成
    category = Category(name="Test Category")
    db.add(category)
    
    # スキルを作成
    skill = Skill(
        name="Test Skill",
        category_id=category.id
    )
    db.add(skill)
    db.commit()
    
    # スキルアセスメントを作成
    assessment = SkillAssessment(
        user_id=user.id,
        skill_id=skill.id,
        proficiency_level=ProficiencyLevel.BEGINNER
    )
    db.add(assessment)
    db.commit()
    
    # 関係性を確認
    db.refresh(user)
    assert len(user.skill_assessments) == 1
    assert user.skill_assessments[0].proficiency_level == ProficiencyLevel.BEGINNER
    assert user.skill_assessments[0].skill.name == "Test Skill"

@pytest.fixture(autouse=True)
def cleanup_db(db: Session):
    """各テスト後にデータベースをクリーンアップ"""
    yield
    db.query(SkillAssessment).delete()
    db.query(Skill).delete()
    db.query(Category).delete()
    db.query(User).delete()
    db.commit()

@pytest.fixture(autouse=True)
def cleanup_users(db):
    """ユーザーデータのクリーンアップ"""
    yield
    try:
        db.query(User).delete()
        db.commit()
    except:
        db.rollback()