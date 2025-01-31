# tests/utils/test_security.py
import pytest
from src.app.utils.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    verify_token
)
from datetime import datetime, timedelta

def test_password_hashing():
    password = "testpassword123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)

def test_token_creation_and_verification():
    username = "testuser"
    token = create_access_token({"sub": username})
    assert token is not None
    
    # トークンの検証
    payload = verify_token(token)
    assert payload["sub"] == username

def test_token_expiration():
    username = "testuser"
    token = create_access_token(
        {"sub": username},
        expires_delta=timedelta(seconds=1)
    )
    
    # トークンが有効な間は検証が成功
    payload = verify_token(token)
    assert payload["sub"] == username
    
    # 有効期限切れを待つ
    import time
    time.sleep(2)
    
    # 有効期限切れのトークンは検証に失敗
    with pytest.raises(Exception):
        verify_token(token)