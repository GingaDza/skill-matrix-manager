# tests/test_migrations.py
from sqlalchemy import inspect

def test_database_tables(test_db_engine):
    inspector = inspect(test_db_engine)
    tables = set(inspector.get_table_names())
    expected_tables = {
        "users",
        "categories",
        "skills",
        "skill_assessments"
    }
    assert tables.intersection(expected_tables) == expected_tables

def test_user_table_columns(test_db_engine):
    inspector = inspect(test_db_engine)
    columns = {col["name"] for col in inspector.get_columns("users")}
    expected_columns = {
        "id",
        "username",
        "email",
        "full_name",
        "hashed_password",
        "is_admin",
        "is_active",
        "created_at",
        "updated_at"
    }
    assert columns == expected_columns

# tests/test_migrations.py
def test_skill_assessment_table_columns(test_db_engine):
    inspector = inspect(test_db_engine)
    columns = {col["name"] for col in inspector.get_columns("skill_assessments")}
    expected_columns = {
        "id",
        "user_id",
        "skill_id",
        "proficiency_level",
        "created_at",
        "updated_at"
    }
    assert columns == expected_columns