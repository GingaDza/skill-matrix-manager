# tests/conftest.py
import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.app.main import app
from src.app.database import Base
from src.app.utils.deps import get_db
from src.app.config import settings
from src.app.models import User
from src.app.utils.security import create_access_token
from src.app.models import Category


# テスト用のデータベースエンジンを作成
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# テスト用のセッションファクトリを作成
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    テストセッション開始時にデータベースを初期化
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    """
    テストケースごとのデータベースセッション
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db):
    """
    テストクライアント
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    del app.dependency_overrides[get_db]

@pytest.fixture
def test_user(db):
    """
    テストユーザーを作成するフィクスチャ
    """
    user = User(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        is_admin=False
    )
    user.set_password("testpassword")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def admin_user(db):
    """
    管理者ユーザーを作成するフィクスチャ
    """
    admin = User(
        username="admin",
        email="admin@example.com",
        full_name="Admin User",
        is_admin=True
    )
    admin.set_password("adminpassword")
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

@pytest.fixture
def auth_headers(test_user):
    """
    一般ユーザー用の認証ヘッダーを生成
    """
    access_token = create_access_token(data={"sub": test_user.username})
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def admin_auth_headers(admin_user):
    """
    管理者ユーザー用の認証ヘッダーを生成
    """
    access_token = create_access_token(data={"sub": admin_user.username})
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def test_db_engine():
    """
    テストデータベースエンジンを提供
    """
    return engine


# tests/conftest.py
@pytest.fixture(autouse=True)
def cleanup_db(db):
    """各テスト後にデータベースをクリーンアップ"""
    yield
    try:
        for table in reversed(Base.metadata.sorted_tables):
            try:
                db.execute(text(f"DELETE FROM {table.name}"))
            except:
                continue
        db.commit()
    except:
        db.rollback()
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_test_time():
    """
    テスト用の固定時刻を設定
    """
    original_now = settings.NOW
    settings.NOW = datetime(2025, 1, 31, 8, 1, 26)
    yield
    settings.NOW = original_now

@pytest.fixture
def test_category(db):
    """テストカテゴリーを作成"""
    category = Category(
        name="Test Category",
        description="Test Description"
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
