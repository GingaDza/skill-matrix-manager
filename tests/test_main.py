# tests/test_main.py
from fastapi.testclient import TestClient
from src.app.main import app

def test_root_endpoint():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Skill Matrix API"}

def test_cors_middleware():
    client = TestClient(app)
    
    # プリフライトリクエストのテスト
    response = client.options(
        "/api/skill-assessments/",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type",
        },
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "*"
    assert "access-control-allow-methods" in response.headers
    assert "access-control-allow-headers" in response.headers

    # 実際のリクエストのテスト
    response = client.get(
        "/api/skill-assessments/",
        headers={"Origin": "http://localhost:3000"},
    )
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "*"