# tests/test_user_auth.py
import pytest
from src.app.models.user import User

class TestUserAuth:
    def test_password_hashing(self):
        u = User(
            username="test_user",
            email="test@example.com",
            full_name="Test User",
            is_admin=False
        )
        u.set_password("test_password")
        assert u.hashed_password is not None
        assert u.hashed_password != "test_password"
        assert u.check_password("test_password")
        assert not u.check_password("wrong_password")

    def test_user_authentication(self):
        u = User(
            username="test_auth_user",
            email="auth_test@example.com",
            full_name="Auth Test User",
            is_admin=False
        )
        u.set_password("test_auth_password")
        assert u.check_password("test_auth_password")
        assert not u.check_password("wrong_password")