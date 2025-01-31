# tests/api/test_skill_assessment.py
from fastapi import status
from src.app.models.enums import ProficiencyLevel

def test_create_assessment_invalid_skill(client, auth_headers):
    assessment_data = {
        "skill_id": 99999,
        "proficiency_level": ProficiencyLevel.INTERMEDIATE.value,
        "evidence": "Test evidence"
    }
    response = client.post(
        "/skill-assessments/",
        json=assessment_data,
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND