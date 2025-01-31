# tests/api/test_auth.py
from fastapi import status
from src.app.schemas.auth import UserCreate

# tests/api/test_auth.py
def test_register_user(client):
    user_data = {
        "username": "newuser",
        "email": "new@example.com",
        "full_name": "New User",
        "password": "newpassword123",
        "is_admin": False
    }
    response = client.post("/api/auth/register", json=user_data)  # URLを修正
    assert response.status_code == status.HTTP_201_CREATED

# tests/api/test_auth.py
def test_login_success(client, test_user):
    response = client.post(
        "/api/auth/login",
        data={  # JSONではなくフォームデータとして送信
            "username": "testuser",
            "password": "testpassword",
        }
    )
    assert response.status_code == 200

# tests/api/test_auth.py
def test_login_invalid_credentials(client):
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword"
    }
    response = client.post(
        "/api/auth/login",  # URLを修正
        data=login_data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED