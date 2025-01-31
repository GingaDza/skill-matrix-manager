# tests/api/test_skill.py
from fastapi import status

# tests/api/test_skill.py
def test_create_skill(client, auth_headers, test_category):
    skill_data = {
        "name": "Test Skill",
        "description": "Test Description",
        "category_id": test_category.id
    }
    response = client.post(
        "/api/skills/",  # URLを修正
        json=skill_data,
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED