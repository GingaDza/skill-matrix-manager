# tests/api/test_category.py
from fastapi import status
# tests/api/test_category.py
# tests/api/test_category.py
def test_create_category(client, auth_headers):
    category_data = {
        "name": "Test Category",
        "description": "Test Description"
    }
    response = client.post(
        "/api/categories/",
        json=category_data,
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED